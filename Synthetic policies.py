"""
Synthetic regulatory and policy documents for POC.
Replace these with your actual internal policy documents in production.
"""

DOCUMENTS = [
    {
        "id": "KYC-001",
        "title": "Know Your Customer (KYC) Policy",
        "content": """
KYC POLICY - INTERNAL DOCUMENT v3.2

1. PURPOSE
The Bank shall verify the identity of all customers before onboarding to prevent money laundering,
terrorist financing, and financial fraud. This policy applies to all retail, corporate, and NRI accounts.

2. CUSTOMER IDENTIFICATION REQUIREMENTS
All individual customers must provide:
- Government-issued photo ID (Aadhaar, PAN, Passport, or Voter ID)
- Proof of address not older than 3 months (utility bill, bank statement, or rent agreement)
- Recent passport-sized photograph
- Mobile number linked to Aadhaar for OTP-based verification

For corporate entities, the following are additionally required:
- Certificate of Incorporation
- Memorandum and Articles of Association
- Board resolution authorising the account opening
- List of beneficial owners holding more than 25% stake

3. RE-KYC REQUIREMENTS
Existing customers must complete Re-KYC every 2 years for high-risk customers,
every 5 years for medium-risk customers, and every 10 years for low-risk customers.
Failure to complete Re-KYC will result in account freezing after 30 days notice.

4. RISK CATEGORISATION
Customers are classified as High, Medium, or Low risk based on:
- Geography of residence (FATF high-risk countries = High)
- Transaction volumes and patterns
- Source of funds declaration
- Politically Exposed Person (PEP) status

5. ENHANCED DUE DILIGENCE (EDD)
High-risk customers require EDD which includes:
- Source of wealth documentation
- Senior management approval for account opening
- Quarterly transaction monitoring reviews
- Face-to-face verification mandatory (video KYC not accepted for High Risk)
"""
    },
    {
        "id": "AML-002",
        "title": "Anti-Money Laundering (AML) Guidelines",
        "content": """
ANTI-MONEY LAUNDERING GUIDELINES v2.1

1. OVERVIEW
The Bank is committed to full compliance with the Prevention of Money Laundering Act (PMLA) 2002
and all subsequent amendments. All staff are responsible for identifying and reporting suspicious activity.

2. SUSPICIOUS TRANSACTION REPORTING (STR)
A Suspicious Transaction Report (STR) must be filed with the Financial Intelligence Unit - India (FIU-IND)
within 7 working days of the transaction being identified as suspicious.
Suspicious indicators include but are not limited to:
- Cash deposits above INR 10 lakhs in a single transaction
- Multiple cash deposits just below the reporting threshold (structuring)
- Transactions inconsistent with the customer's declared business profile
- Sudden large credits followed by immediate withdrawals
- Transactions involving countries on FATF blacklist or greylist

3. CASH TRANSACTION REPORTS (CTR)
All cash transactions above INR 10 lakhs must be reported to FIU-IND via CTR
within 15 days of the end of the month in which the transaction occurred.
This includes both single transactions and aggregated transactions from the same customer
within a calendar month.

4. STAFF OBLIGATIONS
- All staff must complete AML training annually
- Tipping off a customer that an STR has been filed is a criminal offence
- Non-compliance by staff will result in disciplinary action up to and including termination
- The Money Laundering Reporting Officer (MLRO) must be notified of any suspicious activity within 24 hours

5. RECORD KEEPING
All KYC documents and transaction records must be retained for a minimum of 5 years
from the date of account closure or the date of the last transaction, whichever is later.
"""
    },
    {
        "id": "LENDING-003",
        "title": "Retail Lending Credit Policy",
        "content": """
RETAIL LENDING CREDIT POLICY v5.0

1. ELIGIBILITY CRITERIA - PERSONAL LOANS
Minimum eligibility requirements for personal loan applicants:
- Age: 21 to 65 years at loan maturity
- Minimum net monthly income: INR 25,000 for salaried; INR 40,000 for self-employed
- Minimum CIBIL score: 700 (applicants below 650 are automatically declined)
- Minimum employment tenure: 1 year with current employer (salaried); 3 years in business (self-employed)
- Maximum Debt-to-Income (DTI) ratio: 50% including the proposed EMI

2. LOAN PARAMETERS - PERSONAL LOANS
- Minimum loan amount: INR 50,000
- Maximum loan amount: INR 40,00,000 (subject to income and DTI assessment)
- Tenure: 12 to 84 months
- Interest rate: Based on risk-based pricing model, currently 10.5% to 18% per annum
- Processing fee: 1% to 2% of loan amount plus applicable GST

3. HOME LOANS
- Loan-to-Value (LTV) ratio: Maximum 80% for loans above INR 30 lakhs; 85% for loans up to INR 30 lakhs; 90% for loans up to INR 20 lakhs
- Maximum tenure: 30 years
- Mandatory property insurance for the loan tenure
- Minimum CIBIL score: 720
- Pre-payment charges: Nil for floating rate loans; 2% for fixed rate loans

4. CREDIT DECISION AUTHORITY
- Branch Manager: Up to INR 5 lakhs
- Regional Credit Manager: INR 5 lakhs to INR 25 lakhs
- Zonal Credit Committee: INR 25 lakhs to INR 1 crore
- Central Credit Committee: Above INR 1 crore

5. DELINQUENCY AND NPA CLASSIFICATION
- Special Mention Account (SMA-0): Overdue 1-30 days
- SMA-1: Overdue 31-60 days
- SMA-2: Overdue 61-90 days
- Non-Performing Asset (NPA): Overdue beyond 90 days
NPA accounts must be referred to the Recovery team within 5 working days of classification.
"""
    },
    {
        "id": "DATA-004",
        "title": "Data Privacy and Information Security Policy",
        "content": """
DATA PRIVACY AND INFORMATION SECURITY POLICY v4.0

1. SCOPE
This policy applies to all employees, contractors, and third-party vendors who handle
customer data or internal bank data. Violations are subject to disciplinary action and
may result in legal proceedings under the Digital Personal Data Protection Act 2023 (DPDP Act).

2. DATA CLASSIFICATION
All data must be classified into one of four categories:
- Public: Information approved for public release (e.g., annual reports, product brochures)
- Internal: General internal communications and non-sensitive operational data
- Confidential: Customer personal data, financial data, HR records (encryption mandatory at rest and in transit)
- Restricted: Encryption keys, regulatory filings, Board minutes (access on need-to-know basis only, dual authorisation required)

3. CUSTOMER DATA HANDLING
- Customer PII (name, address, phone, account number) must never be stored in unencrypted form
- Customer data must not be downloaded to personal devices under any circumstances
- Sharing customer data with third parties requires a Data Processing Agreement (DPA) and CISO approval
- Customer data must not be used for model training or AI experimentation without explicit consent and legal approval
- Any data breach involving customer PII must be reported to the CISO within 2 hours of discovery

4. AI AND GENERATIVE AI USAGE
- Only approved AI tools listed on the Internal AI Approved Tools Register may be used with bank data
- No customer data or confidential data may be entered into external AI systems including public LLM interfaces
- Synthetic or anonymised data approved by the Data Governance team may be used for AI development and testing
- All AI tools used by the bank must undergo a Privacy Impact Assessment (PIA) before deployment

5. ACCESS CONTROL
- All systems access follows the Principle of Least Privilege
- Privileged access requires Multi-Factor Authentication (MFA)
- Access reviews are conducted quarterly for all system administrators
- Terminated employees' access must be revoked within 4 hours of termination
"""
    },
    {
        "id": "FRAUD-005",
        "title": "Fraud Risk Management Framework",
        "content": """
FRAUD RISK MANAGEMENT FRAMEWORK v2.3

1. FRAUD TYPES COVERED
This framework covers the following fraud categories:
- Internal fraud: Employee misappropriation, unauthorised transactions, data theft
- External fraud: Phishing, card skimming, account takeover, cheque fraud
- Cyber fraud: Business Email Compromise (BEC), ransomware, social engineering
- Identity fraud: Impersonation during account opening or loan application

2. FRAUD DETECTION AND MONITORING
The Bank operates a 24x7 Transaction Monitoring System (TMS) that flags:
- Card transactions above INR 50,000 at unusual hours (11 PM - 6 AM)
- More than 3 failed PIN attempts triggering temporary card block
- Transactions from IP addresses or devices not previously associated with the account
- International transactions from countries flagged as high-risk
All flagged transactions are reviewed by the Fraud Operations team within 1 hour.

3. CUSTOMER NOTIFICATION
- Customers must be notified of any suspicious transaction via SMS and email within 15 minutes
- Customers have the right to raise a fraud dispute within 90 days of the transaction date
- Zero liability for customer if fraud reported within 3 working days (per RBI guidelines)
- Partial liability applies if reported between 4-7 working days

4. FRAUD INCIDENT RESPONSE
Upon confirmed fraud:
- Immediate account freeze to prevent further losses
- FIR must be filed with cybercrime cell within 24 hours for cyber frauds above INR 1 lakh
- Customer must receive provisional credit within 10 working days pending investigation
- Root cause analysis (RCA) must be completed within 30 days

5. STAFF REPORTING
Employees who suspect internal fraud must report to the Vigilance Department directly.
Reporting to line manager is not sufficient if the manager may be involved.
Whistleblower protections apply under the Bank's Whistleblower Policy (REF: HR-WB-001).
Deliberate non-reporting of known fraud is itself a disciplinary offence.
"""
    },
]
