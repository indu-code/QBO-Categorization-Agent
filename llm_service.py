def analyze_transaction(transaction, chart_of_accounts):
    """
    Simulate an LLM analyzing an unfamiliar transaction.
    """

    vendor = transaction["vendor"].lower()
    memo = transaction["memo"].lower()

    # Simulated reasoning for our demo
    if "consulting" in memo or "consulting" in vendor:
        category = "Professional Services"
        confidence = 0.72

    elif "google" in vendor:
        category = "Software & SaaS"
        confidence = 0.80

    elif "uber" in vendor:
        category = "Travel"
        confidence = 0.82

    else:
        category = "Professional Services"
        confidence = 0.45

    return {
        "category": category,
        "confidence": confidence,
        "method": "LLM inference",
        "evidence": "No sufficiently strong historical pattern was found, so deeper reasoning was required.",
        "llm_called": True
    }