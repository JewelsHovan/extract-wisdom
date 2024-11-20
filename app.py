import streamlit as st
import tempfile
import os
from paper_analyzer import PaperAnalyzer
from config import DEFAULT_MODEL, DEFAULT_PROVIDER, MODEL_CONFIGS


def initialize_session_state():
    """Initialize session state variables"""
    if 'selected_provider' not in st.session_state:
        st.session_state.selected_provider = DEFAULT_PROVIDER
    if 'api_keys' not in st.session_state:
        st.session_state.api_keys = {
            'openai': None,
            'openrouter': None,
            'gemini': None
        }
    if 'is_authenticated' not in st.session_state:
        st.session_state.is_authenticated = False


def authenticate_api_key(provider, api_key):
    """Validate the API key based on the provider"""
    try:
        if provider == "openai":
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            client.models.list()
        elif provider == "openrouter":
            from openai import OpenAI
            client = OpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1"
            )
            client.models.list()
        elif provider == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            genai.list_models()
        return True
    except Exception:
        return False


def api_key_form():
    """Display API key input form and handle authentication for multiple providers"""
    with st.sidebar:
        st.subheader("API Configuration")

        # Provider selection
        provider = st.selectbox(
            "Select Provider",
            options=list(MODEL_CONFIGS.keys()),
            key="provider_select"
        )
        st.session_state.selected_provider = provider

        # Show current status for selected provider
        if st.session_state.api_keys[provider]:
            st.success(f"{provider.title()} API Key authenticated!")
            if st.button(f"Clear {provider.title()} API Key"):
                st.session_state.api_keys[provider] = None
                if provider == st.session_state.selected_provider:
                    st.session_state.is_authenticated = False
                st.rerun()

        # Show input form for selected provider
        with st.form(f"{provider}_api_key_form"):
            help_texts = {
                "openai": "Get your API key from https://platform.openai.com/api-keys",
                "openrouter": "Get your API key from https://openrouter.ai/keys",
                "gemini": "Get your API key from Google Cloud Console"
            }
            
            input_api_key = st.text_input(
                f"Enter your {provider.title()} API Key",
                type="password",
                help=help_texts[provider]
            )
            submitted = st.form_submit_button("Submit")

            if submitted and input_api_key:
                if authenticate_api_key(provider, input_api_key):
                    st.session_state.api_keys[provider] = input_api_key
                    if provider == st.session_state.selected_provider:
                        st.session_state.is_authenticated = True
                    st.success(f"{provider.title()} API Key is valid!")
                    st.rerun()
                else:
                    st.error(f"Invalid {provider.title()} API Key")
                    return False

        # Model selection for the chosen provider
        if st.session_state.api_keys[provider]:
            available_models = MODEL_CONFIGS[provider]["models"]
            selected_model = st.selectbox(
                f"Select {provider.title()} Model",
                options=available_models,
                key=f"{provider}_model_select"
            )
            
            # Store the selected model in session state
            if f"{provider}_selected_model" not in st.session_state:
                st.session_state[f"{provider}_selected_model"] = selected_model

        # Return True if the current provider is authenticated
        return bool(st.session_state.api_keys[st.session_state.selected_provider])


def analyze_paper():
    """Main function to handle paper analysis through the Streamlit interface."""
    st.title("Research Paper Analyzer")
    st.write("Upload a PDF file to analyze the paper, and extract insights based on your needs")

    if not api_key_form():
        return

    provider = st.session_state.selected_provider
    model_name = st.session_state[f"{provider}_selected_model"]
    api_key = st.session_state.api_keys[provider]

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    
    if uploaded_file:
        analyze_button = st.button("Analyze Paper")
        if analyze_button:
            try:
                with st.spinner("Processing your file..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name

                    analyzer = PaperAnalyzer(
                        tmp_path, 
                        api_key=api_key,
                        model_name=model_name,
                        provider=provider
                    )
                    
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
    tab1, tab2, tab3, tab4 = st.tabs(["Basic Info", "Background", "Figures Analysis", "Custom Query"])

    with tab1:
        display_basic_info(analyzer)

    with tab2:
        display_background(analyzer)

    with tab3:
        display_figures(analyzer)
        
    with tab4:
        display_custom_query(analyzer)


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


def display_custom_query(analyzer):
    """Display custom query interface and results."""
    st.header("Custom Query")
    st.write("Ask any specific question about the paper")
    
    query = st.text_area("Enter your question:", 
                        placeholder="Example: What are the main contributions of this paper?",
                        help="Enter any question you'd like to ask about the paper.")
    
    if st.button("Get Answer"):
        if query:
            with st.spinner("Analyzing..."):
                try:
                    response = analyzer.custom_query(query)
                    st.write("### Answer")
                    st.write(response)
                except Exception as e:
                    st.error(f"Error processing query: {str(e)}")
        else:
            st.warning("Please enter a question first.")


if __name__ == "__main__":
    st.set_page_config(page_title="Paper Analyzer", layout="wide")
    initialize_session_state()
    analyze_paper()
