FIGURE_INFO_TEMPLATE = """
I have to present a figure to my class. Explain to me in detail what figure {figure_number} is about. Be meticulous and detailed and logical.

Text: {text}

Analyze the figure and provide a detailed explanation."""


FIGURE_COUNT_TEMPLATE = """
Analyze the following academic paper text and count the total number of figures in the paper.

Text: {text}

=> Count the total number of figures (hint look for the last figure number) and respond with just the number."""


FIGURE_CONNECTION_TEMPLATE = """
Analyze the following academic paper text and explain in detail how the results are illustrated by figure {figure_number}.
Be very detailed and logical. Think big picture and small details. Connect key information back to the background.

Text: {text}

Explain in detail how the results are illustrated by figure {figure_number}."""


EXPAND_ANSWER_TEMPLATE = """
Given this answer:
{answer}

Can you expand it and provide more details based on this original text:
{text}

Please provide a more detailed and comprehensive explanation. Do not miss any details."""


EXTRACT_DETAILS_TEMPLATE = """
Extract the details from the following text:
{text}
"""

BACKGROUND_TEMPLATE = """
Extract and summarize the background information from the following text in a detailed and organized manner:

{text}

1. **Detailed Background Explanation:**
   - Summarize the background with a focus on the essential theories, frameworks, and context needed to understand the work.
   - Highlight any historical or research context that influenced the current study.
   - Explain key findings from prior research, identifying any knowledge gaps the paper addresses.

2. **Prerequisite Knowledge:**
   - List and briefly explain any prerequisite concepts, theories, or technical terminology needed to fully understand the background and findings.
   - For each prerequisite, include a brief description or definition to ensure clarity.

3. **Key Topics and Keywords:**
   - Identify important keywords that are crucial for understanding the content of the paper.
   - For each keyword, provide a brief explanation if needed, focusing on terms central to the topic, methodology, and domain of the research.

=> Respond only with the requested information above. Ensure clarity, precision, and completeness to facilitate comprehensive understanding.
"""
