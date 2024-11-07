from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from templates import EXPAND_ANSWER_TEMPLATE, FIGURE_CONNECTION_TEMPLATE, FIGURE_INFO_TEMPLATE
from config import DEFAULT_MODEL

def query_document(document, prompt_template=None, model_name=DEFAULT_MODEL, pydantic_model=None, **prompt_variables):
    # Create LLM instance
    llm = ChatOpenAI(model_name=model_name)
    if pydantic_model:
        llm = llm.with_structured_output(pydantic_model)

    # Create prompt template
    prompt = PromptTemplate(template=prompt_template, input_variables=list(prompt_variables.keys()))
    chain = prompt | llm

    # Run the chain
    response = chain.invoke({
        "text": document,
        **prompt_variables
    })

    return response

def process_figure_answers(document, total_figures: int, model_name: str = DEFAULT_MODEL) -> dict:
    """
    Process and gather information and connections for each figure in the document.
    
    Args:
        document: The loaded document to analyze
        total_figures: Total number of figures to process
        model_name: Name of the LLM model to use
        
    Returns:
        dict: Dictionary containing Information and Connection data for each figure
    """
    try:
        answers = {i: {} for i in range(total_figures)}
        
        for i in range(total_figures):
            print(f"Processing Figure {i+1}...")
            answers[i]["Information"] = query_document(
                document, 
                prompt_template=FIGURE_INFO_TEMPLATE, 
                model_name=model_name, 
                figure_number=i + 1
            )
            answers[i]["Connection"] = query_document(
                document,
                prompt_template=FIGURE_CONNECTION_TEMPLATE,
                model_name=model_name, 
                figure_number=i + 1
            )
        
        return answers
    
    except Exception as e:
        print(f"Error processing figures: {str(e)}")
        raise

def expand_figure_answers(document, answers: dict, model_name: str = DEFAULT_MODEL) -> dict:
    """
    Expand the existing answers with additional context and information.
    
    Args:
        document: The loaded document to analyze
        answers: Dictionary containing the initial answers to expand
        model_name: Name of the LLM model to use
        
    Returns:
        dict: Dictionary containing expanded Information and Connection data
    """
    try:
        expanded_answers = {i: {} for i in range(len(answers))}
        
        for i in range(len(answers)):
            print(f"Expanding Answers for Figure {i+1}...")
            expanded_answers[i]["Information"] = query_document(
                document,
                prompt_template=EXPAND_ANSWER_TEMPLATE,
                model_name=model_name,
                answer=answers[i]["Information"].content,
                text=document
            )
            expanded_answers[i]["Connection"] = query_document(
                document,
                prompt_template=EXPAND_ANSWER_TEMPLATE,
                model_name=model_name,
                answer=answers[i]["Connection"].content,
                text=document
            )
            
        return expanded_answers
        
    except Exception as e:
        print(f"Error expanding answers: {str(e)}")
        raise


def write_analysis_to_file(answers: dict, expanded_answers: dict, output_path: str) -> None:
    """
    Write figure analysis results to a text file.
    
    Args:
        answers: Dictionary containing the initial analysis
        expanded_answers: Dictionary containing the expanded analysis
        output_path: Path where the output file should be saved
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=== Figure Analysis Results ===\n\n")
            
            for i in range(len(answers)):
                f.write(f"### Figure {i+1} ###\n\n")
                
                # Write initial analysis
                f.write("Initial Analysis:\n")
                f.write("-----------------\n")
                f.write(f"Information:\n{answers[i]['Information'].content}\n\n")
                f.write(f"Connection:\n{answers[i]['Connection'].content}\n\n")
                
                # Write expanded analysis
                f.write("Expanded Analysis:\n")
                f.write("-----------------\n")
                f.write(f"Information:\n{expanded_answers[i]['Information'].content}\n\n")
                f.write(f"Connection:\n{expanded_answers[i]['Connection'].content}\n\n")
                
                f.write("\n" + "="*50 + "\n\n")  # Separator between figures
                
        print(f"Analysis written successfully to {output_path}")
        
    except Exception as e:
        print(f"Error writing to file: {str(e)}")
        raise