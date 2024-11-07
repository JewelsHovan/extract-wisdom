# Academic Paper Figure Analyzer

A tool that automatically analyzes academic papers, extracting and explaining figures and their connections to the research. This tool uses LLMs to provide detailed analysis of each figure and its relationship to the paper's content.

## Features

- Extracts paper metadata (title, authors, abstract)
- Identifies and counts total figures in the paper
- Provides detailed analysis of each figure
- Generates comprehensive explanations of how figures relate to the research
- Parallel processing for efficient analysis of multiple figures
- Structured output saved to text files

## Prerequisites

- Python 3.10+
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd [repo-name]
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

## Directory Structure

```
.
├── papers/             # Place your PDF papers here
├── output/            # Analysis results will be saved here
├── paper_analyzer.py  # Main script
├── utils.py          # Utility functions
├── config.py         # Configuration settings
└── templates.py      # Prompt templates
```

## Usage

1. Place your academic paper (PDF format) in the `papers/` directory.

2. Run the analyzer:
```bash
python paper_analyzer.py --paper papers/your_paper.pdf
```

The script will:
- Extract basic paper details (title, authors, abstract)
- Count the total number of figures
- Analyze each figure in detail
- Generate connections between figures and research content
- Save the analysis in `output/figure_analysis_results.txt`

## Output

The analysis will be saved in `output/figure_analysis_results.txt` with the following structure:
- Paper details (title, authors, abstract)
- For each figure:
  - Detailed figure description
  - Connection to research content
  - Expanded analysis

## Configuration

You can modify the following settings in `config.py`:
- `OUTPUT_DIR`: Directory for saving analysis results
- `DEFAULT_MODEL`: GPT model to use for analysis (default: "gpt-4o-mini")

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## TODO

- [ ] Enhance paper content extraction:
  - [ ] Deep dive analysis of Results and Conclusion sections
  - [ ] Extract and analyze Future Work sections
  - [ ] Comprehensive analysis of Background/Introduction
  - [ ] Generate research context summaries
- [ ] Improve figure analysis:
  - [ ] Add support for tables and charts
  - [ ] Generate figure relationships map
  - [ ] Extract figure captions and references
- [ ] Advanced features:
  - [ ] Citation network analysis
  - [ ] Research methodology extraction
  - [ ] Key findings summarization

## Acknowledgments

- Built with LangChain
- Powered by OpenAI's GPT models