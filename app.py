# AI Procurement Assistant Streamlit App

# Import Libraries
import streamlit as st
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Import Custom Modules
from risk_rules import calculate_business_risk
from file_utils import read_uploaded_file
from pdf_utils import create_procurement_report_pdf

# Load environment variables and initialize OpenAI client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ============================================================
# 1. Interface Setup and Configuration
# ============================================================

# ---- Page Configuration ----
st.set_page_config(
    page_title="AI Procurement Assistant",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- Load External Stylesheet ----
def load_css(file_name):
    css_path = Path(__file__).parent / file_name
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("styles.css")

# Function to load prompt templates from files
def load_prompt(filename):
    with open(f"prompts/{filename}", "r", encoding="utf-8") as file:
        return file.read()

# ---- UI Helper: Risk Level Badge ----
def render_risk_badge(risk_level):
    level = (risk_level or "").upper()
    css_class = {"LOW": "risk-low", "MEDIUM": "risk-medium", "HIGH": "risk-high"}.get(level, "")
    icon = {"LOW": "✅", "MEDIUM": "⚠️", "HIGH": "🚨"}.get(level, "•")
    st.markdown(
        f'<div class="risk-badge {css_class}">{icon}&nbsp; Risk Level: {level}</div>',
        unsafe_allow_html=True
    )

# ---- UI Helper: Structured Data Grid ----
def render_extracted_data(extracted_data):
    st.markdown('<p class="section-label">📦 Structured Procurement Data</p>', unsafe_allow_html=True)
    fields = [
        ("🏢 Supplier", extracted_data.get('supplier_name', 'N/A')),
        ("📦 Material", extracted_data.get('material', 'N/A')),
        ("💲 Price", extracted_data.get('price', 'N/A')),
        ("🚚 Delivery (weeks)", extracted_data.get('delivery_time', 'N/A')),
        ("💳 Payment Terms (days)", extracted_data.get('payment_terms', 'N/A')),
        ("📈 Price Change (%)", extracted_data.get('price_change', 'N/A')),
    ]
    cols = st.columns(3)
    for i, (label, value) in enumerate(fields):
        with cols[i % 3]:
            st.markdown(
                f'''<div class="data-card">
                        <div class="data-label">{label}</div>
                        <div class="data-value">{value}</div>
                    </div>''',
                unsafe_allow_html=True
            )

# ---- Header ----
st.markdown(
    '''
    <div class="app-header">
        <div class="app-header-icon">📋</div>
        <div>
            <div class="app-title">AI Procurement Assistant</div>
            <div class="app-subtitle">Analyze supplier risks and price increase requests.</div>
        </div>
    </div>
    ''',
    unsafe_allow_html=True
)

# ---- Sidebar for Analysis Mode Selection ----
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙️ Workspace</div>', unsafe_allow_html=True)
    analysis_mode = st.selectbox(
        "Select Analysis Mode",
        [
            "Analyze Document",
            "Compare Supplier Quotes",
            "Generate Procurement Report",
            "Generate Negotiation Strategy"
        ]
    )
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown(
        '''
        <div class="sidebar-info">
            <p class="sidebar-info-title">Modes</p>
            <ul>
                <li><strong>Analyze Document</strong> — summarize or extract structured data & risk from one file.</li>
                <li><strong>Compare Supplier Quotes</strong> — compare several supplier quotations at once.</li>
                <li><strong>Generate Procurement Report</strong> — produce a full report from analyzed data.</li>
                <li><strong>Generate Negotiation Strategy</strong> — get an AI-suggested negotiation approach.</li>
            </ul>
        </div>
        ''',
        unsafe_allow_html=True
    )

document_texts = []

# ============================================================
# 2. Compare Supplier Quotes Function
# ============================================================
if analysis_mode == "Compare Supplier Quotes":

    st.markdown('<p class="section-label">📥 Upload Supplier Documents</p>', unsafe_allow_html=True)

    document_texts = []                                         # Stores all uploaded supplier documents

    with st.container(border=True):

        # Upload Quotations
        uploaded_files = st.file_uploader(
            "Upload Quotation or Contract",
            type=["txt", "pdf"],
            accept_multiple_files=True
        )

        if uploaded_files:

            # Read all uploaded supplier documents
            try:

                for uploaded_file in uploaded_files:

                    document_text = read_uploaded_file(uploaded_file)

                    document_texts.append({
                        "filename": uploaded_file.name,
                        "content": document_text
                    })

                st.markdown(
                    "".join(
                        f'<span class="file-chip">📄 {doc["filename"]}</span>'
                        for doc in document_texts
                    ),
                    unsafe_allow_html=True
                )

            # Handle expected file-reading errors, such as an empty or unreadable PDF
            except ValueError as error:
                st.error(str(error))

            # Handle unexpected errors while reading uploaded documents
            except Exception as error:
                st.error(
                    f"Unable to read the uploaded documents: {error}"
                )

        compare_clicked = st.button(
            "🔍 Compare Supplier Quotations",
            type="primary"
        )

    if compare_clicked:

        # Prevent comparison if no documents have been uploaded
        if not document_texts:
            st.warning(
                "Please upload at least one supplier quotation."
            )

        else:

            try:

                combined_documents = ""

                # Combine all Uploaded Document Contents into a Single String for Analysis
                for doc in document_texts:

                    combined_documents += f"""
Filename: {doc['filename']}

Content:
{doc['content']}

---
"""

                # Load Prompt for Supplier Quote Comparison
                prompt_template = load_prompt(
                    "supplier_comparison.txt"
                )

                # Format the Prompt with Combined Document Contents
                prompt = prompt_template.format(
                    combined_documents=combined_documents
                )

                # Get OpenAI API Response
                with st.spinner("Comparing supplier quotes..."):

                    response = client.responses.create(
                        model="gpt-4.1-mini",
                        input=prompt
                    )

                # Display AI Recommendations
                st.markdown(
                    '<p class="section-label">📊 Supplier Quote Comparison</p>',
                    unsafe_allow_html=True
                )

                with st.container(border=True):
                    st.write(response.output_text)

                # Allow users to download the comparison as a text file
                st.download_button(
                    label="⬇️ Download Comparison",
                    data=response.output_text,
                    file_name="supplier_comparison.txt",
                    mime="text/plain"
                )

            # Handle all unexpected errors during quotation comparison
            except Exception as error:
                st.error(
                    f"Unable to compare the supplier quotations: {error}"
                )

# ============================================================
# 3. Analyze Document Function
# ============================================================
if analysis_mode == "Analyze Document":

    st.markdown('<p class="section-label">📥 Upload Document</p>', unsafe_allow_html=True)

    uploaded_file = None
    document_text = None
    summarize_clicked = False
    analyze_clicked = False

    with st.container(border=True):
        # Upload Document for Analysis
        uploaded_file = st.file_uploader(
            "Upload Quotation or Contract",
            type=["txt", "pdf"]
        )

        if uploaded_file is not None:

            # Read the uploaded TXT or PDF document
            try:
                document_text = read_uploaded_file(uploaded_file)

            # Handle expected file-reading errors, such as an empty or unreadable PDF
            except ValueError as error:
                st.error(str(error))

            # Handle unexpected errors while reading the uploaded document
            except Exception as error:
                st.error(f"Unable to read the uploaded document: {error}")

            # Only display the action buttons if the document was read successfully
            if document_text is not None:

                col1, col2 = st.columns(2)

                with col1:
                    summarize_clicked = st.button(
                        "📝 Summarize Document",
                        use_container_width=True
                    )

                with col2:
                    analyze_clicked = st.button(
                        "🔎 Analyze Document",
                        use_container_width=True,
                        type="primary"
                    )

    # Generate a document summary
    if summarize_clicked:

        try:
            # Load Prompt for Document Summary
            prompt_template = load_prompt("document_analysis.txt")

            # Format the Prompt with the Document Text
            prompt = prompt_template.format(
                document_text=document_text
            )

            # Get OpenAI API Response
            with st.spinner("Summarizing document..."):
                response = client.responses.create(
                    model="gpt-4.1-mini",
                    input=prompt
                )

            # Display AI Summary
            st.markdown(
                '<p class="section-label">📝 Document Summary</p>',
                unsafe_allow_html=True
            )

            with st.container(border=True):
                st.write(response.output_text)

        # Handle unexpected errors during prompt loading or OpenAI API processing
        except Exception as error:
            st.error(
                f"Unable to summarize the document: {error}"
            )

    # Extract structured procurement data and calculate the business risk
    if analyze_clicked:

        try:
            # Load Prompt for Structured Data Extraction
            prompt_template = load_prompt("document_extraction_json.txt")

            # Format the Prompt with User Inputs
            prompt = prompt_template.format(
                document_text=document_text
            )

            # Get OpenAI API Response
            with st.spinner("Extracting structured procurement data..."):
                response = client.responses.create(
                    model="gpt-4.1-mini",
                    input=prompt
                )

            # Save the extracted text for further processing
            extracted_text = response.output_text

            # Extracted data is expected to be in JSON format, so we parse it into a Python dictionary
            extracted_data = json.loads(extracted_text)         # json.loads() parses the JSON string into a Python dictionary

            # Use session state to store extracted data for later use
            st.session_state["extracted_data"] = extracted_data

            # Display Structured Procurement Data
            render_extracted_data(extracted_data)

            # Business Rules for Risk Assessment
            business_risk_score, risk_level, risk_messages = calculate_business_risk(
                extracted_data
            )

            # Store risk assessment results in session state for later use
            st.session_state["business_risk_score"] = business_risk_score
            st.session_state["risk_level"] = risk_level
            st.session_state["risk_messages"] = risk_messages
            st.session_state["supplier"] = extracted_data.get(
                "supplier_name",
                "N/A"
            )

            st.markdown(
                '<p class="section-label">🧾 Business Rule Checks</p>',
                unsafe_allow_html=True
            )

            # Display Risk Messages based on Business Rules
            for item in risk_messages:

                if item["type"] == "warning":
                    st.warning(item["message"])

                elif item["type"] == "error":
                    st.error(item["message"])

                elif item["type"] == "info":
                    st.info(item["message"])

            # Display Risk Score and Level
            st.markdown(
                '<p class="section-label">📊 Document-Based Risk Score</p>',
                unsafe_allow_html=True
            )

            score_col, badge_col = st.columns([1, 2])

            with score_col:
                st.metric(
                    "Risk Score",
                    f"{business_risk_score}/100"
                )

            with badge_col:
                st.markdown(
                    '<div class="badge-spacer"></div>',
                    unsafe_allow_html=True
                )
                render_risk_badge(risk_level)

        # Handle invalid JSON responses from the AI model
        except json.JSONDecodeError:
            st.error(
                "The AI response was not valid JSON. Please try the analysis again."
            )

        # Handle all other unexpected errors during the analysis workflow
        except Exception as error:
            st.error(
                f"Unable to analyze the document: {error}"
            )

# ============================================================
# 4. Generate Negotiation Strategy Function
# ============================================================
if analysis_mode == "Generate Negotiation Strategy":

    st.markdown(
        '<p class="section-label">🤝 Generate Negotiation Strategy</p>',
        unsafe_allow_html=True
    )

    # Select data source for negotiation strategy generation
    data_source = st.radio(
        "Data Source",
        [
            "Upload new document",
            "Use previous analyzed document"
        ],
        horizontal=True
    )

    if data_source == "Use previous analyzed document":

        # Define all session state values required for generating the strategy
        required_session_data = [
            "extracted_data",
            "business_risk_score",
            "risk_level",
            "risk_messages"
        ]

        # Prevent errors if no document has been analyzed yet or required data is missing
        if not all(key in st.session_state for key in required_session_data):
            st.warning(
                "Please analyze a document first or upload a new document."
            )

        else:

            try:
                # Retrieve extracted data and risk assessment results from session state
                extracted_data = st.session_state["extracted_data"]
                business_risk_score = st.session_state["business_risk_score"]
                risk_level = st.session_state["risk_level"]
                risk_messages = st.session_state["risk_messages"]

                # Load Prompt for Negotiation Strategy
                prompt_template = load_prompt(
                    "negotiation_strategy.txt"
                )

                # Replace all placeholders in the prompt with real values
                prompt = prompt_template.format(
                    extracted_data=json.dumps(
                        extracted_data,
                        indent=2
                    ),
                    business_risk_score=business_risk_score,
                    risk_level=risk_level,
                    risk_messages=json.dumps(
                        risk_messages,
                        indent=2
                    )
                )

                # Get OpenAI API response for negotiation strategy
                with st.spinner("Generating negotiation strategy..."):
                    response = client.responses.create(
                        model="gpt-4.1-mini",
                        input=prompt
                    )

                # Display Negotiation Strategy
                st.markdown(
                    '<p class="section-label">📜 Negotiation Strategy</p>',
                    unsafe_allow_html=True
                )

                with st.container(border=True):
                    st.write(response.output_text)

                # Save the generated negotiation strategy in session state
                negotiation_strategy = response.output_text
                st.session_state["negotiation_strategy"] = negotiation_strategy

                # Retrieve the supplier name for the download file name
                supplier = st.session_state.get(
                    "supplier",
                    "unknown_supplier"
                )

                # Allow users to download the strategy as a text file
                st.download_button(
                    label="⬇️ Download Negotiation Strategy",
                    data=negotiation_strategy,
                    file_name=f"{supplier}_negotiation_strategy.txt",
                    mime="text/plain"
                )

            # Handle all unexpected errors during negotiation strategy generation
            except Exception as error:
                st.error(
                    f"Unable to generate the negotiation strategy: {error}"
                )

    elif data_source == "Upload new document":

        uploaded_file = None
        document_text = None
        generate_clicked = False

        with st.container(border=True):
            # Upload Document for Negotiation Strategy Generation
            uploaded_file = st.file_uploader(
                "Upload Quotation or Contract",
                type=["txt", "pdf"],
                key="negotiation_document_upload"
            )

            # Check if a file has been uploaded
            if uploaded_file is not None:

                try:
                    # Read the uploaded TXT or PDF document
                    document_text = read_uploaded_file(uploaded_file)

                # Handle expected file-reading errors, such as an empty or unreadable PDF
                except ValueError as error:
                    st.error(str(error))

                # Handle unexpected errors while reading the uploaded document
                except Exception as error:
                    st.error(
                        f"Unable to read the uploaded document: {error}"
                    )

                # Only display the button if the document was read successfully
                if document_text is not None:
                    generate_clicked = st.button(
                        "⚡ Generate Strategy from New Document",
                        type="primary"
                    )

        if generate_clicked:

            try:
                # Load Prompt for Structured Data Extraction
                extraction_template = load_prompt(
                    "document_extraction_json.txt"
                )

                # Format the Prompt with User Inputs
                extraction_prompt = extraction_template.format(
                    document_text=document_text
                )

                # Get OpenAI API Response
                with st.spinner(
                    "Extracting structured procurement data..."
                ):
                    extraction_response = client.responses.create(
                        model="gpt-4.1-mini",
                        input=extraction_prompt
                    )

                # Save the extracted text for further processing
                extracted_text = extraction_response.output_text

                # Extracted data is expected to be in JSON format, so we parse it into a Python dictionary
                extracted_data = json.loads(extracted_text)

                # Business Rules for Risk Assessment
                business_risk_score, risk_level, risk_messages = (
                    calculate_business_risk(extracted_data)
                )

                # Store extracted data and risk assessment results in session state
                st.session_state["extracted_data"] = extracted_data
                st.session_state["business_risk_score"] = business_risk_score
                st.session_state["risk_level"] = risk_level
                st.session_state["risk_messages"] = risk_messages
                st.session_state["supplier"] = extracted_data.get(
                    "supplier_name",
                    "unknown_supplier"
                )

                # Load Prompt for Negotiation Strategy
                negotiation_template = load_prompt(
                    "negotiation_strategy.txt"
                )

                # Replace all placeholders in the prompt with real values
                negotiation_prompt = negotiation_template.format(
                    extracted_data=json.dumps(
                        extracted_data,
                        indent=2
                    ),
                    business_risk_score=business_risk_score,
                    risk_level=risk_level,
                    risk_messages=json.dumps(
                        risk_messages,
                        indent=2
                    )
                )

                # Get OpenAI API response for negotiation strategy
                with st.spinner("Generating negotiation strategy..."):
                    response = client.responses.create(
                        model="gpt-4.1-mini",
                        input=negotiation_prompt
                    )

                # Display Negotiation Strategy
                st.markdown(
                    '<p class="section-label">📜 Negotiation Strategy</p>',
                    unsafe_allow_html=True
                )

                with st.container(border=True):
                    st.write(response.output_text)

                # Save the generated negotiation strategy in session state
                negotiation_strategy = response.output_text
                st.session_state["negotiation_strategy"] = negotiation_strategy

                # Retrieve the supplier name from the extracted procurement data
                supplier = extracted_data.get(
                    "supplier_name",
                    "unknown_supplier"
                )

                # Allow users to download the strategy as a text file
                st.download_button(
                    label="⬇️ Download Negotiation Strategy",
                    data=negotiation_strategy,
                    file_name=f"{supplier}_negotiation_strategy.txt",
                    mime="text/plain"
                )

            # Handle invalid JSON responses from the AI model
            except json.JSONDecodeError:
                st.error(
                    "The AI response was not valid JSON. "
                    "Please try generating the strategy again."
                )

            # Handle all other unexpected errors during strategy generation
            except Exception as error:
                st.error(
                    f"Unable to generate the negotiation strategy: {error}"
                )

# ============================================================
# 5. Generate Procurement Report Function
# ============================================================
if analysis_mode == "Generate Procurement Report":

    st.markdown(
        '<p class="section-label">📑 Generate Procurement Report</p>',
        unsafe_allow_html=True
    )

    # Select data source for procurement report generation
    data_source = st.radio(
        "Data Source",
        [
            "Use previous analyzed document",
            "Upload new document"
        ],
        horizontal=True
    )

    if data_source == "Upload new document":

        uploaded_report = None
        document_text = None
        generate_report_clicked = False

        with st.container(border=True):
            # Upload Document for Procurement Report Generation
            uploaded_report = st.file_uploader(
                "Upload Quotation or Contract",
                type=["txt", "pdf"],
                key="procurement_report_document_upload"
            )

            # Check if a file has been uploaded
            if uploaded_report is not None:

                try:
                    # Read the uploaded TXT or PDF document
                    document_text = read_uploaded_file(uploaded_report)

                # Handle expected file-reading errors, such as an empty or unreadable PDF
                except ValueError as error:
                    st.error(str(error))

                # Handle unexpected errors while reading the uploaded document
                except Exception as error:
                    st.error(
                        f"Unable to read the uploaded document: {error}"
                    )

                # Only display the button if the document was read successfully
                if document_text is not None:
                    generate_report_clicked = st.button(
                        "📄 Generate Report from New Document",
                        type="primary"
                    )

        if generate_report_clicked:

            try:
                # Load Prompt for Structured Data Extraction
                extraction_template = load_prompt(
                    "document_extraction_json.txt"
                )

                # Format the Prompt with User Inputs
                extraction_prompt = extraction_template.format(
                    document_text=document_text
                )

                # Get OpenAI API Response
                with st.spinner(
                    "Extracting structured procurement data..."
                ):
                    extraction_response = client.responses.create(
                        model="gpt-4.1-mini",
                        input=extraction_prompt
                    )

                # Save the extracted text for further processing
                extracted_text = extraction_response.output_text

                # Extracted data is expected to be in JSON format, so we parse it into a Python dictionary
                extracted_data = json.loads(extracted_text)

                # Business Rules for Risk Assessment
                business_risk_score, risk_level, risk_messages = (
                    calculate_business_risk(extracted_data)
                )

                # Retrieve the supplier name from the extracted procurement data
                supplier = extracted_data.get(
                    "supplier_name",
                    "unknown_supplier"
                )

                # Store extracted data and risk assessment results in session state
                st.session_state["extracted_data"] = extracted_data
                st.session_state["business_risk_score"] = business_risk_score
                st.session_state["risk_level"] = risk_level
                st.session_state["risk_messages"] = risk_messages
                st.session_state["supplier"] = supplier

                # Load Procurement Report Prompt
                report_prompt_template = load_prompt(
                    "procurement_report.txt"
                )

                # Replace all placeholders in the prompt with real values
                report_prompt = report_prompt_template.format(
                    extracted_data=json.dumps(
                        extracted_data,
                        indent=2
                    ),                                                      # Formats the extracted data as a readable JSON string for the AI model
                    business_risk_score=business_risk_score,               # Inserts the calculated risk score
                    risk_level=risk_level,                                 # Inserts the risk level
                    risk_messages=json.dumps(
                        risk_messages,
                        indent=2
                    ),                                                      # Converts business rule findings into formatted JSON
                    negotiation_strategy=st.session_state.get(
                        "negotiation_strategy",
                        "Not generated yet."
                    )                                                       # Inserts the previously generated negotiation strategy if available
                )

                # Send the completed prompt to OpenAI
                with st.spinner("Generating procurement report..."):
                    report_response = client.responses.create(
                        model="gpt-4.1-mini",
                        input=report_prompt
                    )

                # Save the generated procurement report
                procurement_report = report_response.output_text

                # Display the final procurement report
                st.markdown(
                    '<p class="section-label">📑 AI Procurement Report</p>',
                    unsafe_allow_html=True
                )

                with st.container(border=True):
                    st.write(procurement_report)

                # Generate the procurement report as a PDF using the utility function
                pdf_bytes = create_procurement_report_pdf(
                    procurement_report,
                    supplier
                )

                # Set the file name for the PDF download
                file_name = f"{supplier}_procurement_report.pdf"

                # Allow users to download the generated procurement report as a PDF file
                st.download_button(
                    label="Download Report as PDF",
                    data=pdf_bytes,
                    file_name=file_name,
                    mime="application/pdf"
                )

            # Handle invalid JSON responses from the AI model
            except json.JSONDecodeError:
                st.error(
                    "The AI response was not valid JSON. "
                    "Please try generating the report again."
                )

            # Handle all other unexpected errors during procurement report generation
            except Exception as error:
                st.error(
                    f"Unable to generate the procurement report: {error}"
                )

    elif data_source == "Use previous analyzed document":

        # Define all session state values required for generating the report
        required_session_data = [
            "extracted_data",
            "business_risk_score",
            "risk_level",
            "risk_messages"
        ]

        # Prevent errors if no document has been analyzed yet or required data is missing
        if not all(key in st.session_state for key in required_session_data):
            st.warning(
                "Please analyze a document first."
            )

        # Prevent report generation if no negotiation strategy has been generated yet
        elif "negotiation_strategy" not in st.session_state:
            st.warning(
                "Please generate a negotiation strategy first."
            )

        else:

            try:
                # Retrieve extracted data and risk assessment results from session state for report generation
                extracted_data = st.session_state["extracted_data"]
                business_risk_score = st.session_state["business_risk_score"]
                risk_level = st.session_state["risk_level"]
                risk_messages = st.session_state["risk_messages"]
                negotiation_strategy = st.session_state[
                    "negotiation_strategy"
                ]

                # Retrieve the supplier name for the PDF and download file name
                supplier = st.session_state.get(
                    "supplier",
                    "unknown_supplier"
                )

                # Load Procurement Report Prompt
                report_prompt_template = load_prompt(
                    "procurement_report.txt"
                )

                # Replace all placeholders in the prompt with real values
                report_prompt = report_prompt_template.format(
                    extracted_data=json.dumps(
                        extracted_data,
                        indent=2
                    ),                                                      # Formats the extracted data as a readable JSON string for the AI model
                    business_risk_score=business_risk_score,               # Inserts the calculated risk score
                    risk_level=risk_level,                                 # Inserts the risk level
                    risk_messages=json.dumps(
                        risk_messages,
                        indent=2
                    ),                                                      # Converts business rule findings into formatted JSON
                    negotiation_strategy=negotiation_strategy              # Inserts the previously generated negotiation strategy
                )

                # Send the completed prompt to OpenAI
                with st.spinner("Generating procurement report..."):
                    report_response = client.responses.create(
                        model="gpt-4.1-mini",
                        input=report_prompt
                    )

                # Save the generated procurement report
                procurement_report = report_response.output_text

                # Display the final procurement report
                st.markdown(
                    '<p class="section-label">📑 AI Procurement Report</p>',
                    unsafe_allow_html=True
                )

                with st.container(border=True):
                    st.write(procurement_report)

                # Generate the procurement report as a PDF using the utility function
                pdf_bytes = create_procurement_report_pdf(
                    procurement_report,
                    supplier
                )

                # Set the file name for the PDF download
                file_name = f"{supplier}_procurement_report.pdf"

                # Allow users to download the generated procurement report as a PDF file
                st.download_button(
                    label="Download Report as PDF",
                    data=pdf_bytes,
                    file_name=file_name,
                    mime="application/pdf"
                )

            # Handle all unexpected errors during procurement report generation
            except Exception as error:
                st.error(
                    f"Unable to generate the procurement report: {error}"
                )