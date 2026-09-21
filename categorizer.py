# categorizer.py


# ---------------------------------------------------------
# DEMO TRANSACTIONS
# ---------------------------------------------------------

UNCATEGORIZED_TRANSACTIONS = [

    {
        "id": 1,
        "company_id": "demo-company-001",
        "company_name": "Demo Company",
        "vendor": "AWS",
        "amount": 2400,
        "memo": "AWS cloud services"
    },

    {
        "id": 2,
        "company_id": "demo-company-001",
        "company_name": "Demo Company",
        "vendor": "Uber",
        "amount": 45,
        "memo": "Uber ride"
    },

    {
        "id": 3,
        "company_id": "demo-company-001",
        "company_name": "Demo Company",
        "vendor": "Adobe",
        "amount": 60,
        "memo": "Adobe Creative Cloud"
    },

    {
        "id": 4,
        "company_id": "demo-company-001",
        "company_name": "Demo Company",
        "vendor": "Unknown Consulting",
        "amount": 1200,
        "memo": "Consulting payment"
    }

]


# ---------------------------------------------------------
# HISTORICAL / EXACT MATCH
# ---------------------------------------------------------

def exact_match(transaction):

    vendor = transaction["vendor"]

    historical_categories = {
        "AWS": "Software & SaaS",
        "Uber": "Travel",
        "Adobe": "Software & SaaS"
    }

    if vendor in historical_categories:

        return {
            "category": historical_categories[vendor],
            "confidence": 0.97,
            "method": "Exact historical match",
            "evidence": (
                "Vendor matched a previously categorized transaction "
                "with a consistent historical category."
            ),
            "llm_called": False
        }

    return None


# ---------------------------------------------------------
# PATTERN MATCH
# ---------------------------------------------------------

def pattern_match(transaction):

    vendor = transaction["vendor"].lower()
    memo = transaction["memo"].lower()

    if "consulting" in vendor or "consulting" in memo:

        return {
            "category": "Professional Services",
            "confidence": 0.70,
            "method": "Pattern match",
            "evidence": (
                "Vendor or memo contains a consulting-related pattern."
            ),
            "llm_called": False
        }

    return None


# ---------------------------------------------------------
# LLM FALLBACK
# ---------------------------------------------------------

def llm_fallback(transaction):

    vendor = transaction["vendor"]

    # Demo LLM result.
    # In production this would call the LLM service.

    if vendor == "Unknown Consulting":

        return {
            "category": "Professional Services",
            "confidence": 0.65,
            "method": "LLM inference",
            "evidence": (
                "The transaction appears to be a consulting-related "
                "business expense, but there is insufficient historical "
                "evidence for a high-confidence classification."
            ),
            "llm_called": True,
            "route": "Client confirmation",
            "client_options": [
                "Professional Services",
                "Software & SaaS",
                "Other Expense"
            ]
        }

    return {
        "category": "Other Expense",
        "confidence": 0.40,
        "method": "LLM inference",
        "evidence": (
            "No sufficiently strong historical pattern was found."
        ),
        "llm_called": True,
        "route": "Client confirmation",
        "client_options": [
            "Professional Services",
            "Software & SaaS",
            "Other Expense"
        ]
    }


# ---------------------------------------------------------
# ROUTING
# ---------------------------------------------------------

def route_transaction(result):

    confidence = result["confidence"]

    if confidence >= 0.90:
        return "Auto-post"

    elif confidence >= 0.75:
        return "Firm review"

    else:
        return "Client confirmation"


# ---------------------------------------------------------
# MAIN CATEGORIZATION FUNCTION
# ---------------------------------------------------------

def categorize_transaction(transaction):

    # 1. Try exact historical match

    result = exact_match(transaction)

    if result:

        result["route"] = route_transaction(result)

        return result


    # 2. Try pattern match

    result = pattern_match(transaction)

    if result:

        result["route"] = route_transaction(result)

        # If confidence is low, ask the client
        if result["route"] == "Client confirmation":

            result["client_options"] = [
                "Professional Services",
                "Software & SaaS",
                "Other Expense"
            ]

        return result


    # 3. Use LLM fallback

    result = llm_fallback(transaction)

    if "route" not in result:

        result["route"] = route_transaction(result)

    return result


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    for transaction in UNCATEGORIZED_TRANSACTIONS:

        result = categorize_transaction(transaction)

        print("\nTransaction:")
        print(transaction["vendor"])

        print("Category:", result["category"])
        print("Confidence:", result["confidence"])
        print("Method:", result["method"])
        print("Route:", result["route"])
        print("LLM Called:", result["llm_called"])

        if "client_options" in result:

            print("Client Options:", result["client_options"])