# AI Procurement Assistant

**AI-Powered Supplier Quotation Analysis, Procurement Decision Support & RAG Knowledge Base**

The AI Procurement Assistant is a Streamlit-based web application that uses Large Language Models (OpenAI GPT-4.1-mini), deterministic business rules, and Retrieval-Augmented Generation (RAG) to support procurement professionals throughout the supplier evaluation process.

The application can analyze supplier quotations, extract structured commercial data, identify procurement risks, compare supplier offers, generate negotiation strategies, produce management-ready reports, and build a searchable knowledge base from procurement documents.

The project demonstrates the practical integration of Generative AI into a real-world procurement workflow while combining AI reasoning with explainable business logic and grounded document retrieval.

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

This combines LLM-based document understanding with deterministic procurement rules so that key risk evaluations remain transparent and reproducible.

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

## RAG Procurement Knowledge Base

Upload multiple PDF documents and build a searchable procurement knowledge base using Retrieval-Augmented Generation (RAG).

The RAG pipeline:

1. Extracts text from uploaded PDF documents
2. Splits documents into overlapping text chunks
3. Generates vector embeddings using OpenAI embeddings
4. Stores document chunks and metadata in ChromaDB
5. Converts user questions into embeddings
6. Performs semantic vector search to retrieve the most relevant document chunks
7. Provides the retrieved context to GPT-4.1-mini
8. Generates answers grounded in the uploaded documents
9. Displays the retrieved source documents and chunk references

If the requested information cannot be found in the retrieved document context, the system is instructed to explicitly state that it cannot answer the question based on the provided documents.

### RAG Architecture

```text
PDF Documents
     │
     ▼
Text Extraction
     │
     ▼
Chunking
     │
     ▼
OpenAI Embeddings
     │
     ▼
ChromaDB Vector Store
     │
     │
     ├─────────────────────┐
     │                     │
     │                User Question
     │                     │
     │                     ▼
     │              Question Embedding
     │                     │
     └──────────────► Semantic Search
                           │
                           ▼
                      Top-k Chunks
                           │
                           ▼
                      GPT-4.1-mini
                       /         \
                      ▼           ▼
                   Answer     Source References
```

For learning purposes, the retrieval process was initially implemented manually using OpenAI embeddings, cosine similarity, and top-k retrieval before integrating ChromaDB as the persistent vector store used by the application.

---

# Technology Stack

- Python
- Streamlit
- OpenAI API
  - GPT-4.1-mini
  - OpenAI Embeddings
- ChromaDB
- NumPy
- JSON Structured Output
- ReportLab
- PyPDF
- HTML / CSS
- Custom Business Rule Engine
- Streamlit Session State

---

# Project Structure

```text
ProcurementAssistant/
│
├── app.py
├── rag_utils.py
├── risk_rules.py
├── file_utils.py
├── pdf_utils.py
├── styles.css
├── requirements.txt
├── README.md
├── .gitignore
│
├── prompts/
│   ├── document_analysis.txt
│   ├── document_extraction_json.txt
│   ├── supplier_comparison.txt
│   ├── negotiation_strategy.txt
│   ├── procurement_report.txt
│   └── risk_analysis.txt
│
├── quotation_samples/
│   └── sample supplier documents
│
└── test_rag.py
```

Local environment variables and the local ChromaDB database are excluded from version control through `.gitignore`.

---

# Installation

Clone the repository:

```bash
git clone https://github.com/SaschaK93/ProcurementAssistant.git
cd ProcurementAssistant
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```text
OPENAI_API_KEY=your_api_key
```

Run the application:

```bash
streamlit run app.py
```

---

# Application Workflow

```text
Supplier Documents
        │
        ├──────────────────────────────┐
        │                              │
        ▼                              ▼
Document Analysis              RAG Knowledge Base
        │                              │
        ▼                              ▼
Structured Extraction              Chunking
        │                              │
        ▼                              ▼
Business Rule Engine              Embeddings
        │                              │
        ▼                              ▼
Risk Assessment                   ChromaDB
        │                              │
        ▼                              ▼
Supplier Comparison          Semantic Retrieval
        │                              │
        ▼                              ▼
Negotiation Strategy          Grounded Q&A
        │
        ▼
Procurement Report
```

---

# Screenshots

## Dashboard

<img width="1625" height="527" alt="Dashboard" src="https://github.com/user-attachments/assets/4cefbc97-bec5-4336-aec6-2f24c9a8d47c" />

---

## Structured Procurement Analysis

<img width="1035" height="851" alt="Structured Procurement Analysis" src="https://github.com/user-attachments/assets/fbec39cb-6f40-4933-b3a5-4f4a9169b1f9" />

---

## Negotiation Strategy

<img width="1022" height="798" alt="Negotiation Strategy" src="https://github.com/user-attachments/assets/87cdaa3c-3449-404e-846c-0de7035adcf8" />

---

## Procurement Report

<img width="980" height="841" alt="Procurement Report" src="https://github.com/user-attachments/assets/d10ee122-6027-4a2b-bf03-e8528abd1e98" />

---

## Quotation Comparison

<img width="979" height="849" alt="Quotation Comparison" src="https://github.com/user-attachments/assets/0aa647b4-d210-46ec-a79a-92b72d05bf78" />

---

## RAG Procurement Knowledge Base

<img width="1054" height="812" alt="RAG Procurement Knowledge Base" src="https://github.com/user-attachments/assets/ebe6508c-f492-495d-975f-eab88785a0b0" />

The RAG knowledge base retrieves relevant information from indexed procurement documents and generates grounded answers with retrieved source references.

---

# Current Version

## Version 2.0

Implemented functionality:

- TXT and PDF document support
- AI document summarization
- Structured procurement data extraction
- Procurement dashboard
- Deterministic business rule engine
- Supplier quotation comparison
- Negotiation strategy generation
- Procurement report generation
- PDF export
- RAG procurement knowledge base
- Document chunking with overlap
- OpenAI embeddings
- ChromaDB vector storage
- Semantic document retrieval
- Grounded document Q&A
- Retrieved source references
- Unknown-answer guardrail
- Knowledge base rebuild functionality
- Streamlit Cloud deployment
- Error handling
- Session state management

---

# Engineering Approach

The project was developed incrementally rather than relying on a high-level AI framework from the beginning.

For the RAG implementation, the core retrieval concepts were first implemented manually:

```text
Text
  ↓
Chunks
  ↓
Embeddings
  ↓
Cosine Similarity
  ↓
Top-k Retrieval
  ↓
LLM Context
  ↓
Grounded Answer
```

After validating the retrieval pipeline, the manual vector search was replaced with ChromaDB for persistent vector storage and semantic retrieval.

This approach provided hands-on understanding of the individual components behind a RAG system before introducing a dedicated vector database.

---

# Limitations

Current limitations include:

- PDF text extraction does not include OCR for scanned documents
- The RAG knowledge base currently supports PDF documents
- Retrieved source references identify the retrieved document chunks but are not fine-grained inline citations
- Cloud-hosted local vector storage should not be treated as permanent external database storage
- AI-generated recommendations require human review before procurement decisions are made

---

# Roadmap

Planned future development includes:

- Systematic evaluation of AI-assisted vs. manual procurement workflows
- RAG retrieval and answer-quality evaluation
- Agentic procurement workflows
- Tool calling
- LangGraph-based workflow orchestration
- Human-in-the-loop approval steps
- Additional procurement business rules
- OCR support for scanned PDFs
- Multi-language document support

---

# License

This project is licensed under the MIT License.

---

# Author

**Sascha Knies**

GitHub: https://github.com/SaschaK93