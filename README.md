# Academic Paper Figure Analyzer

A tool that automatically analyzes academic papers, extracting and explaining figures and their connections to the research. This tool uses LLMs to provide detailed analysis of each figure and its relationship to the paper's content.

## Features

- Extracts paper metadata (title, authors, abstract)
- Identifies and counts total figures in the paper
- Provides detailed analysis of each figure
- Generates comprehensive explanations of how figures relate to the research
- Parallel processing for efficient analysis of multiple figures
- Structured output with separate files for metadata, background, and figure analysis

## Prerequisites

- Python 3.10+
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd [repo-name]
```

2. Run the setup script:
```bash
python setup_project.py
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
├── paper_analyzer.py  # Main analysis script
├── utils.py          # Utility functions
├── config.py         # Configuration settings
├── templates.py      # Prompt templates
├── setup.py          # Package setup configuration
└── setup_project.py  # Project setup script
```

## Usage

1. Place your academic paper (PDF format) in the `papers/` directory.

2. Run the analyzer:
```bash
python paper_analyzer.py papers/your_paper.pdf [--output-dir custom/output/path]
```

The script will:
- Extract basic paper details (title, authors, abstract)
- Count the total number of figures
- Analyze each figure in detail
- Generate connections between figures and research content
- Analyze background information
- Save the analysis in separate files under the output directory

## Output Structure

The analysis will be saved in the output directory with the following files:
- `metadata.txt`: Paper details (title, authors, abstract, figure count)
- `background.txt`: Detailed background analysis and prerequisites
- `figures_analysis.txt`: For each figure:
  - Initial analysis (Information and Connection)
  - Expanded analysis with additional context
  - Detailed relationships to research content

## Configuration

You can modify the following settings in `config.py`:
- `PAPER_DIR`: Directory for input PDF papers (default: "papers")
- `OUTPUT_DIR`: Directory for saving analysis results (default: "output")
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