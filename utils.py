from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from templates import EXPAND_ANSWER_TEMPLATE, FIGURE_CONNECTION_TEMPLATE, FIGURE_INFO_TEMPLATE
from config import DEFAULT_MODEL
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures


def query_document(document, prompt_template=None, model_name=DEFAULT_MODEL, pydantic_model=None, **prompt_variables):
    # Create LLM instance
    llm = ChatOpenAI(model_name=model_name)
    if pydantic_model:
        llm = llm.with_structured_output(pydantic_model)

    # Create prompt template
    prompt = PromptTemplate(template=prompt_template,
                            input_variables=list(prompt_variables.keys()))
    chain = prompt | llm

    # Run the chain
    response = chain.invoke({
        "text": document,
        **prompt_variables
    })

    return response


def process_figure_answers(document, total_figures: int, model_name: str = DEFAULT_MODEL) -> dict:
    """Process and gather information and connections for each figure in parallel"""
    try:
        answers = {i: {} for i in range(total_figures)}

        def process_single_figure(i):
            info = query_document(
                document,
                prompt_template=FIGURE_INFO_TEMPLATE,
                model_name=model_name,
                figure_number=i + 1
            )
            conn = query_document(
                document,
                prompt_template=FIGURE_CONNECTION_TEMPLATE,
                model_name=model_name,
                figure_number=i + 1
            )
            return i, {"Information": info, "Connection": conn}

        completed_figures = 0

        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor() as executor:
            future_to_figure = {executor.submit(process_single_figure, i): i
                                for i in range(total_figures)}

            for future in concurrent.futures.as_completed(future_to_figure):
                i, result = future.result()
                answers[i] = result
                completed_figures += 1
                print(
                    f"Progress: {completed_figures}/{total_figures} figures completed (Figure {i+1} done)")

        return answers

    except Exception as e:
        print(f"Error processing figures: {str(e)}")
        raise


def expand_figure_answers(document, answers: dict, model_name: str = DEFAULT_MODEL) -> dict:
    """Expand answers with additional context in parallel"""
    try:
        expanded_answers = {i: {} for i in range(len(answers))}

        def expand_single_figure(i):
            info = query_document(
                document,
                prompt_template=EXPAND_ANSWER_TEMPLATE,
                model_name=model_name,
                answer=answers[i]["Information"].content,
                text=document
            )
            conn = query_document(
                document,
                prompt_template=EXPAND_ANSWER_TEMPLATE,
                model_name=model_name,
                answer=answers[i]["Connection"].content,
                text=document
            )
            return i, {"Information": info, "Connection": conn}

        completed_expansions = 0
        total_expansions = len(answers)

        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor() as executor:
            future_to_figure = {executor.submit(expand_single_figure, i): i
                                for i in range(len(answers))}

            for future in concurrent.futures.as_completed(future_to_figure):
                i, result = future.result()
                expanded_answers[i] = result
                completed_expansions += 1
                print(
                    f"Progress: {completed_expansions}/{total_expansions} expansions completed (Figure {i+1} done)")

        return expanded_answers

    except Exception as e:
        print(f"Error expanding answers: {str(e)}")
        raise


def query_and_expand(
    document,
    prompt_template,
    model_name=DEFAULT_MODEL,
    expansion_model_name=None,
    pydantic_model=None,
    **prompt_variables
):
    """
    Query the document and expand the answer in a single function.

    Args:
        document: The document to query
        prompt_template: Template for the initial query
        model_name: Name of the model to use for initial query
        expansion_model_name: Optional different model to use for expansion
        pydantic_model: Optional Pydantic model for structured output
        **prompt_variables: Additional variables for the prompt template

    Returns:
        The expanded response
    """
    # Get initial response
    initial_response = query_document(
        document,
        prompt_template=prompt_template,
        model_name=model_name,
        pydantic_model=pydantic_model,
        **prompt_variables
    )

    # Extract content based on whether it's a Pydantic model or direct response
    content_to_expand = initial_response.content if hasattr(
        initial_response, 'content') else str(initial_response)

    # Use expansion_model_name if provided, otherwise use the same model as initial query
    expansion_model = expansion_model_name or model_name

    # Expand the response
    expanded_response = query_document(
        document,
        prompt_template=EXPAND_ANSWER_TEMPLATE,
        model_name=expansion_model,
        answer=content_to_expand,
        text=document
    )

    return expanded_response


def write_analysis_to_file(answers: dict, expanded_answers: dict = None, output_path: str = "analysis.txt") -> None:
    """
    Write figure analysis results to a text file.

    Args:
        answers: Dictionary containing the initial analysis
        expanded_answers: Optional dictionary containing the expanded analysis
        output_path: Path where the output file should be saved
    """
    try:
        with open(output_path, 'a', encoding='utf-8') as f:
            f.write("=== Figure Analysis Results ===\n\n")

            for i in range(len(answers)):
                f.write(f"### Figure {i+1} ###\n\n")

                # Write initial analysis
                f.write("Initial Analysis:\n")
                f.write("-----------------\n")
                f.write(f"Information:\n{answers[i]['Information'].content}\n\n")
                f.write(f"Connection:\n{answers[i]['Connection'].content}\n\n")

                # Write expanded analysis only if provided
                if expanded_answers:
                    f.write("Expanded Analysis:\n")
                    f.write("-----------------\n")
                    f.write(f"Information:\n{expanded_answers[i]['Information'].content}\n\n")
                    f.write(f"Connection:\n{expanded_answers[i]['Connection'].content}\n\n")

                f.write("\n" + "="*50 + "\n\n")  # Separator between figures

        print(f"Analysis written successfully to {output_path}")

    except Exception as e:
        print(f"Error writing to file: {str(e)}")
        raise
