# AI Procurement Assistant Streamlit App

# Import Libraries
import streamlit as st
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from risk_rules import calculate_business_risk

# Load environment variables and initialize OpenAI client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
# Compare Supplier Quotes
# ============================================================
if analysis_mode == "Compare Supplier Quotes":

    st.markdown('<p class="section-label">📥 Upload Supplier Documents</p>', unsafe_allow_html=True)

    with st.container(border=True):
        # Upload Quotations
        uploaded_files = st.file_uploader(
            "Upload Quotation or Contract",
            type=["txt"],
            accept_multiple_files=True
        )

        if uploaded_files:
            for uploaded_file in uploaded_files:
                document_text = uploaded_file.read().decode("utf-8")

                document_texts.append({
                    "filename": uploaded_file.name,
                    "content": document_text
                })

            st.markdown(
                "".join(f'<span class="file-chip">📄 {doc["filename"]}</span>' for doc in document_texts),
                unsafe_allow_html=True
            )

        compare_clicked = st.button("🔍 Compare Supplier Quotations", type="primary")

    if compare_clicked:
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
        prompt_template = load_prompt("supplier_comparison.txt")

        # Format the Prompt with Combined Document Contents
        prompt = prompt_template.format(combined_documents=combined_documents)

        # Get OpenAI API Response
        with st.spinner("Comparing supplier quotes..."):
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt
            )
        # Display AI Recommendations
        st.markdown('<p class="section-label">📊 Supplier Quote Comparison</p>', unsafe_allow_html=True)
        with st.container(border=True):
            st.write(response.output_text)

        # Allow users to download the comparison as a text file
        st.download_button(
        label="⬇️ Download Comparison",
        data=response.output_text,
        file_name="supplier_comparison.txt",
        mime="text/plain"
        )  

# ============================================================
# Analyze Document
# ============================================================
if analysis_mode == "Analyze Document":

    st.markdown('<p class="section-label">📥 Upload Document</p>', unsafe_allow_html=True)

    with st.container(border=True):
        # Upload Document for Analysis
        uploaded_file = st.file_uploader(
            "Upload Quotation or Contract",
            type=["txt"]
        )  

        summarize_clicked = False
        analyze_clicked = False

        if uploaded_file is not None:
            document_text = uploaded_file.read().decode("utf-8")

            col1, col2 = st.columns(2)
            with col1:
                summarize_clicked = st.button("📝 Summarize Document", use_container_width=True)
            with col2:
                analyze_clicked = st.button("🔎 Analyze Document", use_container_width=True, type="primary")

    if uploaded_file is not None:

        if summarize_clicked:
            # Load Prompt for Document Analysis
            prompt_template = load_prompt("document_analysis.txt")

            # Format the Prompt with User Inputs
            prompt = prompt_template.format(document_text=document_text)

            # Get OpenAI API Response
            with st.spinner("Summarizing document..."):
                response = client.responses.create(
                    model="gpt-4.1-mini",
                    input=prompt
                )
            # Display AI Recommendations
            st.markdown('<p class="section-label">📝 Document Summary</p>', unsafe_allow_html=True)
            with st.container(border=True):
                st.write(response.output_text)

        if analyze_clicked:
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

            # Display Structured Procurement Data
            try:

                # Extracted data is expected to be in JSON format, so we parse it into a Python dictionary
                extracted_data = json.loads(extracted_text)     # json.loads() to parse the JSON string into a Python dictionary

                # Use session state to store extracted data and risk assessment results for later use
                st.session_state["extracted_data"] = extracted_data

                # Display Structured Procurement Data
                render_extracted_data(extracted_data)

                #  Business Rules for Risk Assessment
                business_risk_score, risk_level, risk_messages = calculate_business_risk(extracted_data)

                # Store risk assessment results in session state for later use
                st.session_state["business_risk_score"] = business_risk_score
                st.session_state["risk_level"] = risk_level
                st.session_state["risk_messages"] = risk_messages
                st.session_state["supplier"] = extracted_data.get('supplier_name', 'N/A')

                st.markdown('<p class="section-label">🧾 Business Rule Checks</p>', unsafe_allow_html=True)
                # Display Risk Messages based on Business Rules
                for item in risk_messages:
                    if item["type"] == "warning":
                        st.warning(item["message"])
                    elif item["type"] == "error":
                        st.error(item["message"])
                    elif item["type"] == "info":
                        st.info(item["message"])

                # Display Risk Score and Level
                st.markdown('<p class="section-label">📊 Document-Based Risk Score</p>', unsafe_allow_html=True)
                score_col, badge_col = st.columns([1, 2])
                with score_col:
                    st.metric("Risk Score", f"{business_risk_score}/100")
                with badge_col:
                    st.markdown('<div class="badge-spacer"></div>', unsafe_allow_html=True)
                    render_risk_badge(risk_level)

            except json.JSONDecodeError:
                st.error("The AI response was not valid JSON.")

# ============================================================
# Generate Negotiation Strategy
# ============================================================
if analysis_mode == "Generate Negotiation Strategy":

    st.markdown('<p class="section-label">🤝 Generate Negotiation Strategy</p>', unsafe_allow_html=True)

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

        # Prevent error if no document has been analyzed yet
        if "extracted_data" not in st.session_state:
            st.warning("Please analyze a document first or upload a new document.")
        else:
            # Retrieve extracted data and risk assessment results from session state
            extracted_data = st.session_state["extracted_data"]
            business_risk_score = st.session_state["business_risk_score"]
            risk_level = st.session_state["risk_level"]
            risk_messages = st.session_state["risk_messages"]

            # Generate negotiation strategy
            prompt_template = load_prompt("negotiation_strategy.txt")

            # Replace all placeholders in the prompt with real values
            prompt = prompt_template.format(
            extracted_data=json.dumps(extracted_data, indent=2),
            business_risk_score=business_risk_score,
            risk_level=risk_level,
            risk_messages=json.dumps(risk_messages, indent=2)
            )

            # Get OpenAI API response for negotiation strategy
            with st.spinner("Generating negotiation strategy..."):
                response = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt
                )

            # Display Negotiation Strategy
            st.markdown('<p class="section-label">📜 Negotiation Strategy</p>', unsafe_allow_html=True)
            with st.container(border=True):
                st.write(response.output_text)
            negotiation_strategy = response.output_text
            st.session_state["negotiation_strategy"] = negotiation_strategy
            supplier = st.session_state.get("supplier", "unknown_supplier")

            # Allow users to download the strategy as a text file
            st.download_button(
            label="⬇️ Download Negotiation Strategy",
            data=negotiation_strategy,
            file_name=f"{supplier}_negotiation_strategy.txt",
            mime="text/plain"
            )  

    elif data_source == "Upload new document":

        with st.container(border=True):
            # Upload Document for Negotiation Strategy Generation
            uploaded_file = st.file_uploader(
                "Upload Quotation or Contract",
                type=["txt"]
            )

            generate_clicked = False

            # Check if a file has been uploaded
            if uploaded_file is not None:

                # Read the uploaded file and decode it to a string
                document_text = uploaded_file.read().decode("utf-8")

                generate_clicked = st.button("⚡ Generate Strategy from New Document", type="primary")

        if uploaded_file is not None and generate_clicked:

                # Load Prompt for Structured Data Extraction
                extraction_template = load_prompt("document_extraction_json.txt")

                # Format the Prompt with User Inputs
                extraction_prompt = extraction_template.format(
                    document_text=document_text
                )

                # Get OpenAI API Response
                with st.spinner("Extracting structured procurement data..."):
                    extraction_response = client.responses.create(
                        model="gpt-4.1-mini",
                        input=extraction_prompt
                    )

                # Save the extracted text for further processing
                extracted_text = extraction_response.output_text

                # Extracted data is expected to be in JSON format, so we parse it into a Python dictionary
                extracted_data = json.loads(extracted_text) 

                #  Business Rules for Risk Assessment
                business_risk_score, risk_level, risk_messages = calculate_business_risk(extracted_data)
                st.session_state["extracted_data"] = extracted_data
                st.session_state["business_risk_score"] = business_risk_score
                st.session_state["risk_level"] = risk_level
                st.session_state["risk_messages"] = risk_messages

                # Load Prompt for Negotiation Strategy
                negotiation_template = load_prompt("negotiation_strategy.txt")

                # Replace all placeholders in the prompt with real values
                negotiation_prompt = negotiation_template.format(
                extracted_data=json.dumps(extracted_data, indent=2),
                business_risk_score=business_risk_score,
                risk_level=risk_level,
                risk_messages=json.dumps(risk_messages, indent=2)
                )

                # Get OpenAI API response for negotiation strategy
                with st.spinner("Generating negotiation strategy..."):
                    response = client.responses.create(
                    model="gpt-4.1-mini",
                    input=negotiation_prompt
                    )

                # Display Negotiation Strategy
                st.markdown('<p class="section-label">📜 Negotiation Strategy</p>', unsafe_allow_html=True)
                with st.container(border=True):
                    st.write(response.output_text)
                negotiation_strategy = response.output_text
                st.session_state["negotiation_strategy"] = negotiation_strategy
                supplier = extracted_data.get('supplier_name', 'unknown_supplier')

                # Allow users to download the strategy as a text file
                st.download_button(
                label="⬇️ Download Negotiation Strategy",
                data=negotiation_strategy,
                file_name=f"{supplier}_negotiation_strategy.txt",
                mime="text/plain"
                )  

# ============================================================
# Generate Procurement Report
# ============================================================
if analysis_mode == "Generate Procurement Report":

        st.markdown('<p class="section-label">📑 Generate Procurement Report</p>', unsafe_allow_html=True)

        # Select data source for negotiation strategy generation
        data_source = st.radio(
            "Data Source",
            [
                "Use previous analyzed document",
                "Upload new document"
            ],
            horizontal=True
        )

        if data_source == "Upload new document":

            with st.container(border=True):
                # Upload Document for Procurement Report Generation
                uploaded_report = st.file_uploader(
                    "Upload Quotation or Contract",
                    type=["txt"]
                )

                generate_report_clicked = False

                # Check if a file has been uploaded
                if uploaded_report is not None:

                    # Read the uploaded file and decode it to a string
                    document_text = uploaded_report.read().decode("utf-8")

                    generate_report_clicked = st.button("📄 Generate Report from New Document", type="primary")

            if uploaded_report is not None and generate_report_clicked:

                    # Load Prompt for Structured Data Extraction
                    extraction_template = load_prompt("document_extraction_json.txt")

                    # Format the Prompt with User Inputs
                    extraction_prompt = extraction_template.format(
                        document_text=document_text
                    )

                    # Get OpenAI API Response
                    with st.spinner("Extracting structured procurement data..."):
                        extraction_response = client.responses.create(
                            model="gpt-4.1-mini",
                            input=extraction_prompt
                        )

                    # Save the extracted text for further processing
                    extracted_text = extraction_response.output_text

                    # Extracted data is expected to be in JSON format, so we parse it into a Python dictionary
                    extracted_data = json.loads(extracted_text) 

                    #  Business Rules for Risk Assessment
                    business_risk_score, risk_level, risk_messages = calculate_business_risk(extracted_data)
                    st.session_state["extracted_data"] = extracted_data
                    st.session_state["business_risk_score"] = business_risk_score
                    st.session_state["risk_level"] = risk_level
                    st.session_state["risk_messages"] = risk_messages

                    # Replace all placeholders in the prompt with real values
                    report_prompt_template = load_prompt("procurement_report.txt")
                    report_prompt = report_prompt_template.format(
                    extracted_data=json.dumps(extracted_data, indent=2),      # json.dumps() to format the extracted data as a JSON string, easier to read for the AI model
                    business_risk_score=business_risk_score,                  # Insert calculated risk score
                    risk_level=risk_level,                                    # Insert risk level (LOW/MEDIUM/HIGH)
                    risk_messages=json.dumps(risk_messages, indent=2),        # Convert business rule findings into formatted JSON
                    negotiation_strategy = st.session_state.get("negotiation_strategy", "Not generated yet.")  # Insert the previously generated negotiation strategy
                    )

                    # Send the completed prompt to OpenAI
                    with st.spinner("Generating procurement report..."):
                        report_response = client.responses.create(
                        model="gpt-4.1-mini",
                        input=report_prompt
                        )

                    # Display the final procurement report
                    st.markdown('<p class="section-label">📑 AI Procurement Report</p>', unsafe_allow_html=True)
                    with st.container(border=True):
                        st.write(report_response.output_text)
                    supplier = st.session_state.get("supplier", "unknown_supplier")

                    # Allow users to download the generated procurement report as a text file
                    st.download_button(
                    label="⬇️ Download Procurement Report",
                    data=report_response.output_text,
                    file_name=f"{supplier}_procurement_report.txt",
                    mime="text/plain"
                    )  

        elif data_source == "Use previous analyzed document":

            # Prevent error if no document has been analyzed yet
            if "extracted_data" not in st.session_state:
                st.warning("Please analyze a document first.")
            elif "negotiation_strategy" not in st.session_state:
                st.warning("Please generate a negotiation strategy first.")
            else:
                # Load Procurement Report Prompt
                report_prompt_template = load_prompt("procurement_report.txt")

                # Retrieve extracted data and risk assessment results from session state for report generation
                extracted_data = st.session_state["extracted_data"]
                business_risk_score = st.session_state["business_risk_score"]
                risk_level = st.session_state["risk_level"]
                risk_messages = st.session_state["risk_messages"]

                # Replace all placeholders in the prompt with real values
                report_prompt = report_prompt_template.format(
                    extracted_data=json.dumps(extracted_data, indent=2),      # json.dumps() to format the extracted data as a JSON string, easier to read for the AI model
                    business_risk_score=business_risk_score,                  # Insert calculated risk score
                    risk_level=risk_level,                                    # Insert risk level (LOW/MEDIUM/HIGH)
                    risk_messages=json.dumps(risk_messages, indent=2),        # Convert business rule findings into formatted JSON
                    negotiation_strategy = st.session_state.get("negotiation_strategy", "Not generated yet.")  # Insert the previously generated negotiation strategy
                    )

                # Send the completed prompt to OpenAI
                with st.spinner("Generating procurement report..."):
                    report_response = client.responses.create(
                    model="gpt-4.1-mini",
                    input=report_prompt
                    )

                # Display the final procurement report
                st.markdown('<p class="section-label">📑 AI Procurement Report</p>', unsafe_allow_html=True)
                with st.container(border=True):
                    st.write(report_response.output_text)
                supplier = st.session_state.get("supplier", "unknown_supplier")

                # Allow users to download the generated procurement report as a text file
                st.download_button(
                    label="⬇️ Download Procurement Report",
                    data=report_response.output_text,
                    file_name=f"{supplier}_procurement_report.txt",
                    mime="text/plain"
                )