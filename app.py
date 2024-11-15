import streamlit as st
import tempfile
import os
from paper_analyzer import PaperAnalyzer

st.set_page_config(page_title="Paper Analyzer", layout="wide")

st.title("Paper Analyzer")
st.write("Upload a PDF file to analyze the paper, and extract insights based on your needs")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    # Create a progress message
    progress_text = st.empty()
    progress_text.write("Processing your file...")
    
    try:
        # Create a temporary file to store the uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        # Create analyzer instance
        analyzer = PaperAnalyzer(tmp_path)
        
        # Create tabs for different analyses
        tab1, tab2, tab3 = st.tabs(["Basic Info", "Background", "Figures Analysis"])
        
        # Run analysis
        analyzer.load_document()
        analyzer.extract_basic_info()
        
        # Display basic information in the first tab
        with tab1:
            st.subheader("Paper Details")
            st.write(f"**Title:** {analyzer.details_response.title}")
            st.write(f"**Authors:** {analyzer.details_response.authors}")
            st.write(f"**Number of Figures:** {analyzer.figure_count_response.total_figures}")
            st.write("**Abstract:**")
            st.write(analyzer.details_response.abstract)
        
        # Background analysis in second tab
        with tab2:
            st.subheader("Background Analysis")
            with st.spinner("Analyzing background..."):
                analyzer.analyze_background()
                with open(os.path.join(analyzer.output_dir, "background.txt"), 'r') as f:
                    background_content = f.read()
                st.write(background_content)
        
        # Figures analysis in third tab
        with tab3:
            st.subheader("Figures Analysis")
            with st.spinner("Analyzing figures..."):
                analyzer.analyze_figures()
                with open(os.path.join(analyzer.output_dir, "figures_analysis.txt"), 'r') as f:
                    figures_content = f.read()
                st.write(figures_content)
        
        # Clear the progress message
        progress_text.empty()
        
        # Cleanup temporary file
        os.unlink(tmp_path)
        
    except Exception as e:
        st.error(f"An error occurred during analysis: {str(e)}")


