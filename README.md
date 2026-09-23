# AI Procurement Assistant

**AI-Powered Supplier Quotation Analysis and Procurement Decision Support**

The AI Procurement Assistant is a Streamlit-based web application that leverages Large Language Models (OpenAI GPT-4.1-mini) to support procurement professionals throughout the supplier evaluation process.

The application combines AI-driven document understanding with deterministic business rules to analyze supplier quotations, identify commercial risks, compare supplier offers, generate negotiation strategies, and produce management-ready procurement reports.

The project demonstrates the practical integration of Generative AI into procurement workflows while maintaining explainable business logic for risk assessment.

---

# Features

## Document Analysis

- Upload TXT and PDF supplier quotations or contracts
- AI-generated document summaries
- Structured procurement data extraction
- Procurement dashboard for extracted information

---

## Business Rule Engine

Automatically evaluates procurement risks using predefined business rules.

Current evaluations include:

- Payment terms
- Incoterms
- Penalty clauses
- Delivery time
- Price increase
- Minimum order quantity
- Critical procurement information

Each analysis generates:

- Risk Score (0–100)
- Risk Level (Low / Medium / High)
- Detailed business rule findings

---

## Supplier Quote Comparison

Compare multiple supplier quotations simultaneously.

Comparison categories include:

- Price
- Delivery time
- Payment terms
- Incoterms
- Penalty clauses
- Minimum order quantity
- Price validity
- Overall supplier recommendation

---

## Negotiation Strategy Generation

Generate AI-assisted supplier negotiation strategies based on:

- Extracted procurement data
- Business rule evaluation
- Risk assessment

Generated outputs include:

- Executive summary
- Negotiation priorities
- Supplier questions
- Counter proposals
- Draft supplier email

---

## Procurement Report Generation

Generate management-ready procurement reports containing:

- Executive summary
- Supplier overview
- Commercial terms
- Business rule findings
- Risk assessment
- Procurement concerns
- Negotiation recommendations

Reports can be exported directly as professionally formatted PDF documents.

---

# Technology Stack

- Python
- Streamlit
- OpenAI API (GPT-4.1-mini)
- JSON Structured Output
- ReportLab (PDF Generation)
- PyPDF
- HTML / CSS
- Custom Business Rule Engine
- Streamlit Session State

---

# Project Structure

```text
AI-Procurement-Assistant/

│
├── app.py
├── risk_rules.py
├── file_utils.py
├── pdf_utils.py
├── styles.css
├── requirements.txt
├── README.md
│
├── prompts/
│   ├── document_analysis.txt
│   ├── document_extraction_json.txt
│   ├── supplier_comparison.txt
│   ├── negotiation_strategy.txt
│   └── procurement_report.txt
│
└── .env
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Procurement-Assistant.git

cd AI-Procurement-Assistant
```

Install the required packages

```bash
pip install -r requirements.txt
```

Create a `.env` file

```text
OPENAI_API_KEY=your_api_key
```

Run the application

```bash
streamlit run app.py
```

---

# Workflow

```text
Supplier Quotation / Contract
            │
            ▼
      Document Upload
            │
            ▼
    AI Document Analysis
            │
            ▼
Structured Data Extraction
            │
            ▼
 Business Rule Evaluation
            │
            ▼
     Procurement Risk Score
            │
            ▼
 Supplier Quote Comparison
            │
            ▼
 Negotiation Strategy
            │
            ▼
 Procurement Report (PDF)
```

---

# Screenshots

## Dashboard
<img width="1625" height="527" alt="image" src="https://github.com/user-attachments/assets/4cefbc97-bec5-4336-aec6-2f24c9a8d47c" />

---

## Structured Procurement Analysis
<img width="1035" height="851" alt="image" src="https://github.com/user-attachments/assets/fbec39cb-6f40-4933-b3a5-4f4a9169b1f9" />

---

## Negotiation Strategy
<img width="1022" height="798" alt="image" src="https://github.com/user-attachments/assets/87cdaa3c-3449-404e-846c-0de7035adcf8" />

---

## Procurement Report
<img width="980" height="841" alt="image" src="https://github.com/user-attachments/assets/d10ee122-6027-4a2b-bf03-e8528abd1e98" />

---

## Quotation Comparison
<img width="979" height="849" alt="image" src="https://github.com/user-attachments/assets/0aa647b4-d210-46ec-a79a-92b72d05bf78" />

---
# Current Version

## Version 1.1

Implemented functionality:

- TXT document support
- PDF document support
- AI document summarization
- Structured procurement data extraction
- Procurement dashboard
- Business rule engine
- Supplier quotation comparison
- Negotiation strategy generation
- Procurement report generation
- Professional PDF export
- Modern Streamlit user interface
- Modular project architecture
- Error handling
- Session state management

---

# Future Improvements

Planned enhancements include:

- DOCX report export
- Excel export
- Interactive procurement dashboards
- Additional procurement business rules
- OCR support for scanned PDFs
- Supplier scoring dashboard
- Multi-language document support

---

# License

This project is licensed under the MIT License.

---

# Author

**Sascha Knies**

GitHub

https://github.com/SaschaK93
