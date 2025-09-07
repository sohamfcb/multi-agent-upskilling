from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool

from googleapiclient.discovery import build

from dotenv import load_dotenv
import requests
import os

load_dotenv()

youtube_api_key=os.getenv("YOUTUBE_API_KEY")
ALPHA_VANTAGE_API_KEY=os.getenv("ALPHA_VANTAGE_API_KEY")

search_tool = DuckDuckGoSearchRun(region="us-en")

wiki_api_wrapper=WikipediaAPIWrapper(top_k_results=5)
wiki_tool=WikipediaQueryRun(api_wrapper=wiki_api_wrapper,
                            description="A tool to explain things in text format. Use this tool if you think the user's asked concept is best explained through text.",
                            name="wiki_tool")

@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """
    Perform a basic arithmetic operation on two numbers.
    Supported operations: add, sub, mul, div
    """
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed"}
            result = first_num / second_num
        else:
            return {"error": f"Unsupported operation '{operation}'"}
        
        return {"first_num": first_num, "second_num": second_num, "operation": operation, "result": result}
    except Exception as e:
        return {"error": str(e)}

@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA') 
    using Alpha Vantage with API key in the URL.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    r = requests.get(url)
    return r.json()


@tool
def fetch_coursera_courses(query: str):
    """
    Fetch courses from Coursera API based on a search query.
    
    Args:
        query (str): Search query for courses
        
    Returns:
        str: Formatted course information including names, descriptions, and URLs
    """
    url = f"https://api.coursera.org/api/courses.v1?q=search&query={query}&fields=name,description,partnerIds,slug"

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        courses = data.get("elements", [])

        results = []
        for course in courses[:5]:  # Limit to top 5 results
            name = course.get("name", "Unknown Course")
            desc = course.get("description", "No description available")
            slug = course.get("slug", "")
            course_url = f"https://www.coursera.org/learn/{slug}" if slug else "URL not available"

            results.append(f"**Name: {name}**\nDescription: {desc}\n🔗 [Course Link]({course_url})")

        return "\n\n".join(results) if results else "No courses found."

    else:
        return f"Error: {response.status_code} - {response.text}"


@tool
def youtube_search(query, max_results=5):
    """
    Search YouTube videos using the YouTube API.
    
    Args:
        query (str): Search query for videos
        max_results (int): Maximum number of results to return
        
    Returns:
        str: Formatted video information including titles, descriptions, and URLs
    """
    youtube = build("youtube", "v3", developerKey=youtube_api_key)

    search_response = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=max_results,
        type="video"
    ).execute()

    video_data = []

    for video in search_response.get("items", []):
        video_id = video['id']['videoId']
        title = video['snippet']['title']
        description = video['snippet']['description']
        channel_title = video['snippet']['channelTitle']
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        video_data.append(
            f"**Title: {title}**\n📺 Channel: {channel_title}\n📝 Description: {description}\n🔗 [Watch Here]({video_url})"
        )

    return "\n\n".join(video_data) if video_data else "No videos found."

# # def custom_state_modifier(state):
# #     """
# #     Allows the agent to use tools, but if no tool is applicable,
# #     it generates a response using its own knowledge.
# #     """
# #     if "tool" not in state:  # If no tool is chosen
# #         state["output"] = model.invoke(state["messages"])  # Let the model generate response
# #     return state

# def custom_state_modifier(state):
#     """
#     Modifies the state to either use tools or generate a response from the model.
    
#     Args:
#         state (dict): Current state of the agent
        
#     Returns:
#         dict: Modified state
#     """
#     if "messages" not in state:
#         state["messages"] = []  # Ensure messages list exists

#     if "tool" not in state:  # If no tool is chosen, generate response
#         model_response = model.invoke(state["messages"])
#         state["messages"].append(AIMessage(content=model_response.content))  # Append AI response

#     return state

# def generate_text(query):
#     """
#     Generate text response from the model's knowledge base.
    
#     Args:
#         query: Input query for the model
        
#     Returns:
#         str: Generated text response
#     """
#     return model.invoke(query).content 


def get_tools():
    tools = [search_tool, get_stock_price, calculator, wiki_tool, fetch_coursera_courses, youtube_search]
    return tools
