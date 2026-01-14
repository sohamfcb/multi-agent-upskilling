from schema.resume_models import IsResume, SkillGaps, CandidateDetails

from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
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
    

   
def get_suggestions(text,agent,api_keys: dict):
    try:
        # Get career summary from resume
        career_summary = get_resume_details(text=text, model='gemini')
        if not career_summary:
            raise ValueError("Could not extract career details from resume")

        # Initialize models
        model = ChatGoogleGenerativeAI(
            model='gemini-2.0-flash',
            api_key=api_keys["GEMINI_API_KEY"]
        )

        # Extract job roles
        job_roles = career_summary.job_role
        if not job_roles:
            raise ValueError("No job roles found in resume")

        # Get industry trends
        industry_trends = agent.invoke({
            "messages": f"Do a detailed search for the required skillsets and current trend for the job roles {job_roles} and provide your answers in a clean format."
        })
        
        if not industry_trends or "messages" not in industry_trends:
            raise ValueError("Could not fetch industry trends")

        industry_trends_results = str(industry_trends.get("messages")[-2].content) + str(industry_trends.get("messages")[-1].content)

        # Analyze skill gaps
        parser_skill_gaps = PydanticOutputParser(pydantic_object=SkillGaps)
        agent_prompt_template = PromptTemplate(
            template="""
                You will be given a career summary of the candidate which is as follows: \n{career_summary}.\n 
                You will also be given required skillsets and industry trends for one or more than one job roles {job_roles} 
                which is as follows: {industry_trends_results}. \n 
                You need to compare the candidates profile with the industry trends and find out the skill gaps, 
                strengths, weaknesses, areas of improvement.\n {format_instructions}
            """,
            input_variables=["career_summary", "job_roles", "industry_trends_results"],
            partial_variables={
                "format_instructions": parser_skill_gaps.get_format_instructions()
            }
        )

        skill_gaps_chain = agent_prompt_template | model | parser_skill_gaps
        skill_gaps = skill_gaps_chain.invoke({
            "career_summary": career_summary,
            "job_roles": job_roles,
            "industry_trends_results": industry_trends_results
        })

        # Summarize skill gaps
        str_parser = StrOutputParser()
        summarize_skill_gaps_prompt = PromptTemplate(
            template="""
                You will receive details about a candidate's weaknesses: {weaknesses} 
                and areas of improvement: {areas_of_improvement}. 
                You will also get the job role/roles that suit(s) the candidate: {job_roles}. 
                You need to summarize the candidate's weaknesses and areas of improvement in a single paragraph.
            """,
            input_variables=["weaknesses", "areas_of_improvement", "job_roles"]
        )

        model_groq = ChatGroq(
            model="openai/gpt-oss-120b",
            api_key=api_keys["GROQ_API_KEY"]
        )

        summarize_skill_gaps_chain = summarize_skill_gaps_prompt | model_groq | str_parser
        skill_gaps_summary = summarize_skill_gaps_chain.invoke({
            "weaknesses": skill_gaps.weaknesses,
            "areas_of_improvement": skill_gaps.areas_of_improvement,
            "job_roles": job_roles
        })

        # Fetch learning resources
        agent_prompt_template_fetch_materials = """
            You will receive summarized details about a candidate's weaknesses and areas of improvement: {skill_gaps_summary}. 
            You will also get the job role/roles that suit(s) the candidate: {job_roles}. 
            You need to fetch relevant courses or resources or information according to the candidate's weaknesses 
            and areas of improvement and the job role. Use the tools at your disposal. Use multiple tools if and when required. 
            Provide courses, materials from the internet and youtube video links and also provide URLs for each. 
            Use all the tools given to you: `youtube_search_tool`, `text_generator_tool`, `duckduckgo_search_tool`, 
            `coursera_search_tool` and `wiki_tool`. Address the candidate as a second person.
        """

        resources = agent.invoke({
            "messages": agent_prompt_template_fetch_materials.format(
                skill_gaps_summary=skill_gaps_summary, 
                job_roles=job_roles
            )
        })

        return resources

    except Exception as e:
        print(f"Error in get_suggestions: {str(e)}")
        raise