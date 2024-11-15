#!/usr/bin/env python3

import argparse
import dotenv
import os
from pydantic import BaseModel, Field
from langchain_community.document_loaders import PyMuPDFLoader

from config import OUTPUT_DIR, DEFAULT_MODEL
from utils import query_document, process_figure_answers, expand_figure_answers, write_analysis_to_file, query_and_expand
from templates import FIGURE_COUNT_TEMPLATE, EXTRACT_DETAILS_TEMPLATE, BACKGROUND_TEMPLATE

# Pydantic models
class FiguresCount(BaseModel):
    total_figures: int = Field(description="Total number of figures in the paper")

class PaperDetails(BaseModel):
    title: str = Field(description="Title of the paper")
    abstract: str = Field(description="Abstract of the paper")
    authors: str = Field(description="Authors of the paper")

class PaperAnalyzer:
    def __init__(self, pdf_path: str, api_key: str, output_dir: str = OUTPUT_DIR):
        """Initialize PaperAnalyzer with pdf path and output directory."""
        self.pdf_path = pdf_path
        self.base_filename = os.path.splitext(os.path.basename(pdf_path))[0]
        self.output_dir = os.path.join(output_dir, self.base_filename)
        self.document = None
        self.details_response = None
        self.figure_count_response = None

        # Set OPENAI API key
        os.environ["OPENAI_API_KEY"] = api_key
        
        # Create output directory structure
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_document(self):
        """Load the PDF document."""
        loader = PyMuPDFLoader(self.pdf_path)
        self.document = loader.load()
    
    def extract_basic_info(self):
        """Extract paper details and figure count."""
        self.figure_count_response = query_document(
            self.document,
            prompt_template=FIGURE_COUNT_TEMPLATE,
            model_name=DEFAULT_MODEL,
            pydantic_model=FiguresCount
        )
        
        self.details_response = query_document(
            self.document,
            prompt_template=EXTRACT_DETAILS_TEMPLATE,
            model_name=DEFAULT_MODEL,
            pydantic_model=PaperDetails
        )
    
    def write_metadata(self):
        """Write paper metadata to a separate file."""
        metadata_file = os.path.join(self.output_dir, "metadata.txt")
        with open(metadata_file, 'w', encoding='utf-8') as f:
            f.write(f"Title: {self.details_response.title}\n")
            f.write(f"Abstract: {self.details_response.abstract}\n")
            f.write(f"Authors: {self.details_response.authors}\n")
            f.write(f"Number of figures: {self.figure_count_response.total_figures}\n")
    
    def analyze_background(self):
        """Extract and write background information."""
        print(f"Extracting background information...")
        background_response = query_and_expand(
            self.document,
            prompt_template=BACKGROUND_TEMPLATE,
            model_name=DEFAULT_MODEL,
            text=self.document
        )
        
        background_file = os.path.join(self.output_dir, "background.txt")
        with open(background_file, 'w', encoding='utf-8') as f:
            f.write(background_response.content)
    
    def analyze_figures(self):
        """Process and write figure analysis."""
        print(f"Analyzing figures...")
        answers = process_figure_answers(
            self.document, 
            self.figure_count_response.total_figures
        )
        
        expanded_answers = expand_figure_answers(self.document, answers)
        
        figures_file = os.path.join(self.output_dir, "figures_analysis.txt")
        write_analysis_to_file(answers, expanded_answers, figures_file)
    
    def analyze(self):
        """Run the complete analysis pipeline."""
        try:
            print("Loading document...")
            self.load_document()
            
            print("Extracting basic information...")
            self.extract_basic_info()
            
            print("Writing metadata...")
            self.write_metadata()
            
            print("Analyzing background...")
            self.analyze_background()
            
            print("Analyzing figures...")
            self.analyze_figures()
            
            print("Analysis completed successfully!")
            
        except Exception as e:
            print(f"Error during analysis: {str(e)}")
            raise

def main():
    dotenv.load_dotenv()
    
    parser = argparse.ArgumentParser(description="Analyze scientific papers and extract figures information")
    parser.add_argument("pdf_path", help="Path to the PDF file to analyze")
    parser.add_argument("--output-dir", help="Custom output directory", default=OUTPUT_DIR)
    
    args = parser.parse_args()
    
    try:
        analyzer = PaperAnalyzer(args.pdf_path, args.output_dir)
        analyzer.analyze()
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
