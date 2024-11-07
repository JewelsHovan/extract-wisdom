#!/usr/bin/env python3

import argparse
import dotenv
import os
from pydantic import BaseModel, Field
from langchain_community.document_loaders import PyMuPDFLoader

from config import OUTPUT_DIR, DEFAULT_MODEL
from utils import query_document, process_figure_answers, expand_figure_answers, write_analysis_to_file
from templates import FIGURE_COUNT_TEMPLATE, EXTRACT_DETAILS_TEMPLATE

# Pydantic models
class FiguresCount(BaseModel):
    total_figures: int = Field(description="Total number of figures in the paper")

class PaperDetails(BaseModel):
    title: str = Field(description="Title of the paper")
    abstract: str = Field(description="Abstract of the paper")
    authors: str = Field(description="Authors of the paper")

def analyze_paper(pdf_path: str, output_dir: str = OUTPUT_DIR) -> None:
    """
    Analyze a scientific paper and extract its details and figures.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the document
    loader = PyMuPDFLoader(pdf_path)
    document = loader.load()
    
    # Extract figure count
    figure_count_response = query_document(
        document,
        prompt_template=FIGURE_COUNT_TEMPLATE,
        model_name=DEFAULT_MODEL,
        pydantic_model=FiguresCount
    )
    
    # Extract paper details
    details_response = query_document(
        document,
        prompt_template=EXTRACT_DETAILS_TEMPLATE,
        model_name=DEFAULT_MODEL,
        pydantic_model=PaperDetails
    )
    
    # Print initial results
    print(f"Title: {details_response.title}")
    print(f"Abstract: {details_response.abstract}")
    print(f"Authors: {details_response.authors}")
    print(f"Number of figures: {figure_count_response.total_figures}")
    
    # Process figures
    print(f"Extracting information about each figure from the paper {details_response.title}...")
    answers = process_figure_answers(document, figure_count_response.total_figures)
    
    print(f"Expanding the answers for {details_response.title}...")
    expanded_answers = expand_figure_answers(document, answers)
    
    # Get base filename without extension and create new output filename
    base_filename = os.path.splitext(os.path.basename(pdf_path))[0]
    output_file = os.path.join(output_dir, f"{base_filename}_analysis.txt")
    print(f"Writing the analysis to {output_file}...")
    write_analysis_to_file(answers, expanded_answers, output_file)

def main():
    # Load environment variables
    dotenv.load_dotenv()
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Analyze scientific papers and extract figures information")
    parser.add_argument("pdf_path", help="Path to the PDF file to analyze")
    parser.add_argument("--output-dir", help="Custom output directory", default=OUTPUT_DIR)
    
    args = parser.parse_args()
    
    try:
        analyze_paper(args.pdf_path, args.output_dir)
        print("Analysis completed successfully!")
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
