from schema.resume_models import IsResume, SkillGaps, CandidateDetails

from langchain.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key=os.getenv('GROQ_API_KEY')
os.environ["OPENAI_API_KEY"]=os.getenv('OPENAI_API_KEY','')
gemini_api_key=os.getenv('GEMINI_API_KEY')

models_dict = {
    "groq": ChatGroq(model="openai/gpt-oss-120b", api_key=groq_api_key),
    "openai": ChatOpenAI(model="gpt-4o"),
    "gemini": ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=gemini_api_key)
}

def get_resume_details(text, model_name="groq"):
    """
    Extract and analyze details from a resume text.
    
    Args:
        text (str): The resume text to analyze
        model (str): The model to use for analysis ("groq", "gpt", or "gemini")
        
    Returns:
        CandidateDetails: Extracted candidate details
        str: Error message if document is not a resume
    """
    model=models_dict.get(model_name)
    if not model:
        raise Exception("No model name passed.")

    # Initialize resume validation parser
    parser_is_resume=PydanticOutputParser(pydantic_object=IsResume)

    # Create prompt for resume validation
    prompt1=PromptTemplate(
        template="You'll receive a text below. You have to figure out whether it is a proper resume or not. \n {text} \n {format_instructions}",
        input_variables=["text"],
        partial_variables={
            "format_instructions":parser_is_resume.get_format_instructions()
        }
    )

    # Initialize candidate details parser
    parser_candidate_details=PydanticOutputParser(pydantic_object=CandidateDetails)

    # Create prompt for extracting candidate details
    prompt2=PromptTemplate(
        template="You'll receive a resume below. You have to extract the essential details from the resume: \n {text} \n {format_instructions}",
        input_variables=["text"],
        partial_variables={
            "format_instructions":parser_candidate_details.get_format_instructions()
        }
    )

    # Validate if document is a resume
    chain1 = prompt1 | model | parser_is_resume
    response_is_resume=chain1.invoke({"text":text})

    if response_is_resume.is_resume=="no":
        return {
            "message": "The document you uploaded is not a valid resume."
        }

    else:
        # Extract candidate details
        chain2 = prompt2 | model | parser_candidate_details
        return chain2.invoke({"text":text})