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

Please provide a more detailed and comprehensive explanation."""


EXTRACT_DETAILS_TEMPLATE = """
Extract the details from the following text:
{text}
"""