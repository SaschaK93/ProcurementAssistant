**AI Procurement Assistant
AI-Powered Supplier Quotation Analysis and Procurement Decision Support**

An AI-powered procurement assistant built with **Python**, **Streamlit**, and the **OpenAI API**.

The application helps procurement professionals analyze supplier quotations, extract structured procurement data, identify procurement risks, compare supplier offers, generate negotiation strategies, and create executive procurement reports.

---

## Features

### Document Analysis

- Summarize supplier quotations and contracts
- Extract structured procurement data using AI
- Display procurement information in a structured dashboard

### Business Rule Engine

Automatically evaluates procurement risks based on predefined business rules.

Examples include:

- Missing payment terms
- Missing Incoterms
- Missing penalty clauses
- Long delivery times
- Price increase evaluation
- Minimum order quantity checks

Each document receives:

- Risk Score (0–100)
- Risk Level (Low / Medium / High)
- Detailed findings

---

### Supplier Quote Comparison

Compare multiple supplier quotations simultaneously.

The assistant compares:

- Price
- Delivery time
- Payment terms
- Incoterms
- Penalty clauses
- Minimum order quantity
- Price validity

---

### Negotiation Strategy

Generate an AI-assisted negotiation strategy based on:

- Structured procurement data
- Business rule evaluation
- Risk assessment

The strategy includes:

- Executive summary
- Negotiation priorities
- Supplier questions
- Counter proposals
- Draft supplier email

---

### Procurement Report

Generate a management-ready procurement report including:

- Supplier overview
- Commercial terms
- Business rule findings
- Risk assessment
- Procurement concerns
- Negotiation recommendations
- Executive summary

Reports can be downloaded directly from the application.

---

## Technology Stack

- Python
- Streamlit
- OpenAI API (GPT-4.1-mini)
- JSON Structured Output
- Custom Business Rule Engine
- HTML/CSS
- Session State

---

## Project Structure

```text
AI-Procurement-Assistant/

│
├── app.py
├── risk_rules.py
│
├── prompts/
│   ├── document_analysis.txt
│   ├── document_extraction_json.txt
│   ├── supplier_comparison.txt
│   ├── negotiation_strategy.txt
│   └── procurement_report.txt
│
├── styles.css
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Procurement-Assistant.git

cd AI-Procurement-Assistant
```

Install dependencies

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

## Workflow

```text
Supplier Quotation
        │
        ▼
Document Analysis
        │
        ▼
Structured Data Extraction
        │
        ▼
Business Rule Evaluation
        │
        ▼
Risk Assessment
        │
        ▼
Negotiation Strategy
        │
        ▼
Executive Procurement Report
```

---

## Screenshots

### Dashboard

*(Add screenshot)*

### Structured Procurement Analysis

*(Add screenshot)*

### Negotiation Strategy

*(Add screenshot)*

### Procurement Report

*(Add screenshot)*

---

## Current Version

**Version 1.0**

Implemented features:

- Document Analysis
- Structured Data Extraction
- Business Rule Engine
- Supplier Quote Comparison
- Negotiation Strategy Generation
- Procurement Report Generation
- Report Download
- Modern Streamlit Dashboard

---

## Roadmap

### Version 1.1

- PDF document support
- DOCX export
- Excel export
- Improved report templates
- Dashboard visualizations
- Enhanced prompt engineering
- Additional procurement business rules

---

## License

This project is licensed under the MIT License.

---

## Author

**Sascha Knies**

GitHub:
https://github.com/SaschaK93
