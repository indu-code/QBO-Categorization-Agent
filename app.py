from flask import Flask, render_template, redirect, url_for

from categorizer import (
    UNCATEGORIZED_TRANSACTIONS,
    categorize_transaction
)

from qbo_service import (
    propose_categorization,
    approve_categorization
)


app = Flask(__name__)


# ---------------------------------------------------------
# DEMO STATE
# ---------------------------------------------------------

categorization_cache = {}

proposals = {}

audit_log = []


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

@app.route("/")
def home():

    transactions = []

    for transaction in UNCATEGORIZED_TRANSACTIONS:

        transaction_id = transaction["id"]

        # Get categorization result
        if transaction_id in categorization_cache:

            result = categorization_cache[transaction_id]

        else:

            result = categorize_transaction(transaction)

            categorization_cache[transaction_id] = result


        # Create proposal if it does not exist
        if transaction_id not in proposals:

            proposals[transaction_id] = propose_categorization(
                transaction,
                result
            )


        transactions.append({
            **transaction,
            **result,
            "status": proposals[transaction_id]["status"]
        })


    # Count LLM calls
    llm_calls = sum(
        1
        for result in categorization_cache.values()
        if result.get("llm_called", False)
    )


    total_transactions = len(
        UNCATEGORIZED_TRANSACTIONS
    )


    no_llm_calls = (
        total_transactions - llm_calls
    )


    return render_template(
        "index.html",
        transactions=transactions,
        llm_calls=llm_calls,
        no_llm_calls=no_llm_calls
    )


# ---------------------------------------------------------
# TRANSACTION DETAIL
# ---------------------------------------------------------

@app.route(
    "/transaction/<int:transaction_id>"
)
def transaction_detail(transaction_id):

    transaction = next(
        (
            item
            for item in UNCATEGORIZED_TRANSACTIONS
            if item["id"] == transaction_id
        ),
        None
    )


    if transaction is None:

        return "Transaction not found", 404


    # Get categorization result
    if transaction_id in categorization_cache:

        result = categorization_cache[transaction_id]

    else:

        result = categorize_transaction(transaction)

        categorization_cache[transaction_id] = result


    # Make sure proposal exists
    if transaction_id not in proposals:
        proposals[transaction_id] = propose_categorization(
        transaction,
        result
        )

    proposal = proposals[transaction_id]

# Keep proposal aligned with the latest categorization result
    if proposal["status"] == "Pending Approval":
        proposal["new_category"] = result["category"]


    return render_template(
    "transaction.html",
    transaction=transaction,
    result=result,
    proposal=proposal,
    audit_log=[
        entry
        for entry in audit_log
        if entry["transaction_id"] == transaction_id
    ]
)


# ---------------------------------------------------------
# FIRM APPROVAL
# ---------------------------------------------------------

@app.route("/approve/<int:transaction_id>", methods=["POST"])
def approve(transaction_id):
    if transaction_id not in proposals:
        return "Proposal not found", 404

    proposal = proposals[transaction_id]

    proposal = approve_categorization(proposal)
    proposals[transaction_id] = proposal

    audit_log.append({
        "transaction_id": transaction_id,
        "company_id": proposal["company_id"],
        "company_name": proposal["company_name"],
        "vendor": proposal["vendor"],
        "action": "Categorization approved and posted",
        "new_category": proposal["new_category"],
        "status": proposal["status"]
    })

    return redirect(
        url_for(
            "transaction_detail",
            transaction_id=transaction_id
        )
    )


# ---------------------------------------------------------
# CLIENT CONFIRMATION
# ---------------------------------------------------------

@app.route(
    "/client-confirm/<int:transaction_id>/<int:option>",
    methods=["GET", "POST"]
)
def client_confirm(transaction_id, option):

    # Find transaction
    transaction = next(
        (
            item
            for item in UNCATEGORIZED_TRANSACTIONS
            if item["id"] == transaction_id
        ),
        None
    )


    if transaction is None:

        return "Transaction not found", 404


    # Get categorization result
    if transaction_id in categorization_cache:

        result = categorization_cache[transaction_id]

    else:

        result = categorize_transaction(transaction)

        categorization_cache[transaction_id] = result


    # Get available client options
    options = result.get(
        "client_options",
        []
    )


    if not options:

        return "No client options available", 400


    # Validate selected option
    if option < 1 or option > len(options):

        return "Invalid option", 400


    # Selected category
    selected_category = options[
        option - 1
    ]


    # Create proposal if necessary
    if transaction_id not in proposals:

        proposals[transaction_id] = propose_categorization(
            transaction,
            result
        )


    # Update proposal
    proposals[transaction_id][
        "new_category"
    ] = selected_category


    proposals[transaction_id][
        "status"
    ] = "Client Confirmed"


    # Return to transaction page
    return redirect(
        url_for(
            "transaction_detail",
            transaction_id=transaction_id
        )
    )

@app.route("/send-confirmation/<int:transaction_id>", methods=["POST"])
def send_confirmation(transaction_id):
    if transaction_id not in proposals:
        return "Proposal not found", 404

    proposals[transaction_id]["confirmation_sent"] = True
    proposals[transaction_id]["confirmation_channel"] = "Email"

    return redirect(
        url_for(
            "transaction_detail",
            transaction_id=transaction_id
        )
    )

if __name__ == "__main__":

    app.run(debug=True)