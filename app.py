import streamlit as st
import tempfile
import os
from paper_analyzer import PaperAnalyzer


def initialize_session_state():
    """Initialize session state variables"""
    if 'api_key' not in st.session_state:
        st.session_state.api_key = None
    if 'is_authenticated' not in st.session_state:
        st.session_state.is_authenticated = False


def authenticate_api_key(api_key):
    """Validate the API key by making a minimal API call"""
    from openai import OpenAI
    try:
        client = OpenAI(api_key=api_key)
        # Make a minimal API call to verify the key
        client.models.list()
        return True
    except Exception:
        return False


def api_key_form():
    """Display API key input form and handle authentication"""
    with st.sidebar:
        st.subheader("OpenAI API Key")
# 
        # Show current status
        if st.session_state.is_authenticated:
            st.success("API Key authenticated!")
            if st.button("Clear API Key"):
                st.session_state.api_key = None
                st.session_state.is_authenticated = False
                st.experimental_rerun()
            return True  # This is fine

        # Show input form
        with st.form("api_key_form"):
            input_api_key = st.text_input(
                "Enter your OpenAI API Key",
                type="password",
                help="Get your API key from https://platform.openai.com/api-keys"
            )
            submitted = st.form_submit_button("Submit")

            if submitted and input_api_key:
                if authenticate_api_key(input_api_key):
                    st.session_state.api_key = input_api_key
                    st.session_state.is_authenticated = True
                    st.success("API Key authenticated successfully!")
                    return True  # Changed from st.experimental_rerun()
                else:
                    st.error("Invalid API Key. Please try again.")
                    return False

        if not st.session_state.is_authenticated:
            st.warning(
                "Please enter your OpenAI API key to use the application.")
            return False

        return st.session_state.is_authenticated  # Modified return statement


def analyze_paper():
    """Main function to handle paper analysis through the Streamlit interface."""
    st.title("Research Paper Analyzer")
    st.write("Upload a PDF file to analyze the paper, and extract insights based on your needs")

    if not api_key_form():
        return

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    
    if uploaded_file:
        analyze_button = st.button("Analyze Paper")
        if analyze_button:
            try:
                with st.spinner("Processing your file..."):
                    # Create temp file with context manager
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name

                    analyzer = PaperAnalyzer(tmp_path, api_key=st.session_state.api_key)
                    
                    # Perform analysis
                    analyzer.load_document()
                    basic_info = analyzer.extract_basic_info()
                    background = analyzer.analyze_background()
                    figures = analyzer.analyze_figures()

                    # Display results in tabs
                    display_analysis_results(analyzer, basic_info, background, figures)

            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
            finally:
                # Cleanup temp file
                if 'tmp_path' in locals():
                    os.unlink(tmp_path)

def display_analysis_results(analyzer, basic_info, background, figures):
    """Display analysis results in organized tabs."""
    tab1, tab2, tab3 = st.tabs(["Basic Info", "Background", "Figures Analysis"])

    with tab1:
        display_basic_info(analyzer)

    with tab2:
        display_background(analyzer)

    with tab3:
        display_figures(analyzer)

def display_basic_info(analyzer):
    """Display basic paper information."""
    st.subheader("Paper Details")
    details = {
        "Title": analyzer.details_response.title,
        "Authors": analyzer.details_response.authors,
        "Number of Figures": analyzer.figure_count_response.total_figures,
        "Abstract": analyzer.details_response.abstract
    }
    
    for key, value in details.items():
        if key != "Abstract":
            st.write(f"**{key}:** {value}")
    st.write("**Abstract:**")
    st.write(details["Abstract"])

def display_background(analyzer):
    """Display background analysis."""
    st.subheader("Background Analysis")
    with st.spinner("Loading background analysis..."):
        background_path = os.path.join(analyzer.output_dir, "background.txt")
        if os.path.exists(background_path):
            with open(background_path, 'r') as f:
                st.write(f.read())
        else:
            st.warning("Background analysis not available")

def display_figures(analyzer):
    """Display figures analysis."""
    st.subheader("Figures Analysis")
    with st.spinner("Loading figures analysis..."):
        figures_path = os.path.join(analyzer.output_dir, "figures_analysis.txt")
        if os.path.exists(figures_path):
            with open(figures_path, 'r') as f:
                st.write(f.read())
        else:
            st.warning("Figures analysis not available")


if __name__ == "__main__":
    st.set_page_config(page_title="Paper Analyzer", layout="wide")
    initialize_session_state()
    analyze_paper()
