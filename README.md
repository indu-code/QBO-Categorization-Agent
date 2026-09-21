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

**Categorization Strategy**

1. Exact Historical Match
Checks whether the vendor has been consistently categorized before. Strong historical matches avoid unnecessary LLM calls.

2. Pattern Match
Uses transaction information such as vendor and memo to identify recognizable patterns.

3. LLM Inference
Used when deterministic evidence is insufficient. The agent returns a suggested category, confidence score, and supporting evidence.

4. Confidence-Based Routing

Confidence	Action
≥ 90%	Auto-post
75–89%	Firm review
< 75%	Client confirmation

These thresholds are demonstration values and would be calibrated using historical accounting data in production.

**Client Confirmation**

For low-confidence transactions, the client receives structured category options.

Example:

Unknown Consulting — ₹1,200

1. Professional Services
2. Software & SaaS
3. Other Expense

The selected category is added to the posting proposal.

**Approval Workflow**

AI recommendations are never written directly to QuickBooks.

AI Recommendation
       ↓
Posting Proposal
       ↓
Review / Confirmation
       ↓
Explicit Approval
       ↓
QBO Write

This creates a controlled boundary between AI-generated recommendations and accounting system changes.

**Features**

Historical transaction matching
Pattern-based categorization
LLM fallback
Confidence scoring
Confidence-based routing
Client confirmation workflow
Posting proposal
Explicit approval before write
Transaction review dashboard
Transaction-level reasoning/evidence

**Project Structure**

qbo-categorization-agent/
│
├── app.py
├── categorizer.py
├── qbo_service.py
├── llm_service.py
├── templates/
│   ├── index.html
│   └── transaction.html
├── README.md
└── requirements.txt

**Tech Stack**

Python
Flask
Jinja2
HTML/CSS
LLM-based classification
QuickBooks Online integration architecture

**Run Locally**

git clone YOUR_GITHUB_REPOSITORY_URL
cd qbo-categorization-agent

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
python app.py

Then open:

http://127.0.0.1:5000

**Current Prototype Scope**

This prototype focuses on the core categorization and approval workflow.

Transaction data is currently seeded/mock data, and the QuickBooks write is represented through a service layer rather than a live QBO connection.

The service layer can later be connected to the real QBO OAuth/API flow.

**Production Extensions**

A production implementation would add:

QuickBooks OAuth 2.0
MCP-based QBO connector
Per-company realmId isolation
Secure token storage and refresh handling
QBO rate-limit handling
SyncToken validation before writes
Idempotency and duplicate-write protection
Persistent database
Audit trail
Production email confirmation
Multi-tenant firm/client isolation
Confidence calibration and model evaluation

**Note**

This repository is a prototype demonstrating the categorization, confidence-routing, client-confirmation, and approval workflow.

The current QBO write operation is mocked and does not modify a real QuickBooks Online company.

