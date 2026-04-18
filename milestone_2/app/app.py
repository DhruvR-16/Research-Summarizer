import streamlit as st
import os
import sys
import time
from fpdf import FPDF, XPos, YPos

# Add project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)

from milestone_2.graph import run_research

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Professional Research Analysis Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INITIALIZE SESSION STATE ---
if "research_results" not in st.session_state:
    st.session_state.research_results = None

# --- PDF GENERATION LOGIC ---
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title Section
    pdf.set_font("helvetica", 'B', 16)
    pdf.cell(0, 10, "RESEARCH ANALYSIS REPORT", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(10)
    
    # Body Content
    pdf.set_font("helvetica", size=11)
    
    # Formal text processing
    clean_text = text.replace("#", "").replace("**", "").replace("__", "")
    pdf.multi_cell(0, 8, clean_text.encode('latin-1', 'replace').decode('latin-1'))
    
    return bytes(pdf.output())

# --- CUSTOM CLEAN CSS (Minimalist Black/Grey) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    section[data-testid="stSidebar"] {
        background-color: #1a1c23;
        border-right: 1px solid #333;
    }
    h1, h2, h3 {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    .stTextInput > div > div > input {
        background-color: #1a1c23;
        color: white;
        border: 1px solid #444;
        border-radius: 4px;
    }
    .stButton > button {
        background-color: #ffffff;
        color: #000000;
        border-radius: 4px;
        font-weight: 600;
        border: none;
        transition: 0.2s ease-in-out;
        width: 100%;
        text-transform: uppercase;
        font-size: 0.8rem;
    }
    .stButton > button:hover {
        background-color: #f0f0f0;
        color: #000000;
        border: none;
    }
    .report-container {
        background-color: #161a21;
        padding: 2.5rem;
        border-radius: 8px;
        border: 1px solid #333;
        margin-top: 1.5rem;
        line-height: 1.7;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: SYSTEM CONFIGURATION ---
with st.sidebar:
    st.title("System Status")
    st.markdown("---")
    
    # Check for credentials in environment
    groq_ready = bool(os.getenv("GROQ_API_KEY"))
    tavily_ready = bool(os.getenv("TAVILY_API_KEY"))

    if groq_ready:
        st.success("✅ Groq Intelligence Linked")
    else:
        st.error("❌ Groq Logic Offline")
    
    if tavily_ready:
        st.success("✅ Tavily Search Linked")
    else:
        st.warning("⚠️ Tavily Search Offline")
    
    st.markdown("---")
    extract_facts = st.toggle("Technical Fact Extraction", value=True, help="Isolate key metrics and statistics into a structured table")
    
    if st.button("Initialize New Session", key="session_reinit_btn"):
        st.session_state.research_results = None
        st.rerun()

# --- MAIN INTERFACE: RESEARCH CONTROL ---
st.title("Intelligent Research Assistant")
research_query = st.text_input("Specify Research Objective", placeholder="Enter technical topic, industry trend, or breakthrough area", help="The autonomous agent will retrieve and reason across multiple sources to fulfill this query")

control_col1, control_col2 = st.columns([1, 1])

with control_col1:
    initiate_research = st.button("Initiate Analysis", key="main_init_btn")

with control_col2:
    terminate_process = st.button("Terminate Process", key="main_term_btn")

if terminate_process:
    st.session_state.research_results = None
    st.warning("Process terminated by operator.")
    st.rerun()

if initiate_research:
    # Retrieve credentials from system environment
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    if not groq_api_key:
        st.error("Authentication Error: Groq API Key is not detected in your system environment.")
    elif not research_query:
        st.warning("Input Required: Please define a valid research objective.")
    else:
        with st.status("System Status: Autonomous Processing Underway", expanded=True) as status:

            try:
                st.write("Current Phase: Data Acquisition & Source Discovery")
                # Invoke LangGraph Backend
                execution_state = run_research(research_query, extract_facts=extract_facts)
                
                # Persist results to state memory
                st.session_state.research_results = execution_state
                status.update(label="Analysis Completed Successfully", state="complete", expanded=False)
                
            except Exception as e:
                status.update(label="Critical System Error", state="error")
                st.error(f"Execution Failure: {e}")

# --- ANALYTICAL OUTPUT PRESENTATION ---
if st.session_state.research_results:
    results_data = st.session_state.research_results
    
    st.divider()
    st.markdown("### Synthesized Intelligence Report")
    
    st.markdown('<div class="report-container">', unsafe_allow_html=True)
    st.markdown(results_data.get("final_report", "Generating synthesized findings..."))
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Formal Export Utilities
    report_content = results_data.get("final_report", "")
    pdf_payload = create_pdf(report_content)
    
    st.download_button(
        label="Export Results as PDF Document",
        data=pdf_payload,
        file_name="research_analysis_report.pdf",
        mime="application/pdf",
        key="formal_pdf_export_btn"
    )

    # Technical Metadata (Collapsible)
    with st.expander("Technical Metadata & Audit Trail"):
        audit_col1, audit_col2 = st.columns(2)
        with audit_col1:
            st.markdown("**Execution Workflow:**")
            for entry in results_data.get("steps", []):
                st.markdown(f"- {entry}")
        with audit_col2:
            st.markdown("**Validated Sources:**")
            for uri in results_data.get("sources", []):
                st.markdown(f"- {uri}")
else:
    if not research_query:
        st.info("System Ready: Define a research objective above to begin autonomous intelligence synthesis.")
