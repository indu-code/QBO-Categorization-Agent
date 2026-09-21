import uuid


def propose_categorization(transaction, result):
    """
    Create a proposal scoped to one QBO company.
    """

    return {
        "transaction_id": transaction["id"],
        "company_id": transaction["company_id"],
        "company_name": transaction["company_name"],
        "vendor": transaction["vendor"],
        "amount": transaction["amount"],
        "old_category": "Uncategorized",
        "new_category": result["category"],
        "confidence": result["confidence"],
        "status": "Pending Approval",
        "qbo_response": None
    }


def approve_categorization(proposal):
    """
    Simulate the approved write to QuickBooks.
    """

    request_id = str(uuid.uuid4())[:8].upper()

    proposal["status"] = "Approved & Posted"

    proposal["qbo_response"] = {
        "success": True,
        "request_id": request_id,
        "qbo_transaction_id": f"QBO-{proposal['transaction_id']:04d}",
        "message": "Category update successfully posted to QuickBooks."
    }

    return proposal