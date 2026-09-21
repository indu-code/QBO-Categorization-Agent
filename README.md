# QBO Categorization Agent

An AI-assisted transaction categorization and approval workflow for
QuickBooks Online (QBO).

The system analyzes uncategorized transactions, uses historical
evidence and pattern matching before falling back to LLM inference,
assigns a confidence score, and routes each transaction to the
appropriate next step.

## Overview

Accounting teams often spend significant time manually reviewing and
categorizing uncategorized transactions.

This prototype demonstrates a workflow where:

1. Historical matches are checked first.
2. Pattern-based evidence is used when available.
3. LLM inference is used when deterministic evidence is insufficient.
4. A confidence score is assigned to the classification.
5. The transaction is routed based on confidence.
6. Low-confidence transactions can be sent for client confirmation.
7. A posting proposal is created before any write.
8. An explicit approval is required before the transaction is posted.

