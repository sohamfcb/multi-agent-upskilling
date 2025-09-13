from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

from typing import Any, Optional

from helper import get_resume_details
from services.workflows.tools import get_tools

import sqlite3

from dotenv import load_dotenv
import os

import logging

load_dotenv()
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")

def init_chat_logger():
    os.makedirs("logs", exist_ok=True)  # ensure logs directory exists
    chat_logger = logging.getLogger("chatbot.responses")
    chat_logger.setLevel(logging.INFO)

    # Avoid duplicate handlers
    if not chat_logger.handlers:
        handler = logging.FileHandler("logs/chatbot_responses.log")
        formatter = logging.Formatter(
            "%(asctime)s - [%(threadName)s] - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        chat_logger.addHandler(handler)

    return chat_logger

chat_logger = init_chat_logger()

CHECKPOINTER = InMemorySaver()
TOOLS = get_tools()
TOOL_NODE = ToolNode(tools=TOOLS)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    resume_text: Optional[str]
    resume_parsed: Optional[dict] 

# Insert this wrapper function into agent_model.py
def get_resume_details_node(state: ChatState) -> dict[str, Any]:
    """
    LangGraph node wrapper for helper.get_resume_details.
    - Looks for resume text in the most recent HumanMessage (or state['resume_text']).
    - Calls helper.get_resume_details(...) and returns either:
        {"messages": [AIMessage("...not a resume...")]}   # on invalid doc
      or
        {"messages": [AIMessage("...ack...")], "resume_parsed": parsed_result}
    """
    messages = state.get("messages", [])
    # Find latest human message content
    resume_text = None
    # Prefer an explicit key if some earlier node inserted it
    if isinstance(state, dict) and state.get("resume_text"):
        resume_text = state["resume_text"]
    else:
        # find last human message in messages
        for m in reversed(messages):
            # msg.type property may exist on your BaseMessage model
            if getattr(m, "type", None) == "human" or isinstance(m, HumanMessage):
                resume_text = getattr(m, "content", None)
                break

    if not resume_text:
        # no resume text found -> tell user how to upload/attach
        return {"messages": [AIMessage("I couldn't find the resume text. Please upload or paste your resume content.")]}
    
    # call your helper (this can be blocking; LangGraph supports sync node functions)
    try:
        parsed = get_resume_details(resume_text, model_name="groq")
    except Exception as exc:
        # model or parsing error -> bubble a friendly error
        return {"messages": [AIMessage(f"Error while parsing resume: {exc}")]}
    
    # your get_resume_details returns either a dict with {"message": "..."} for not-resume
    if isinstance(parsed, dict) and parsed.get("message"):
        # Send that message as an AIMessage to the user
        return {"messages": [AIMessage(parsed["message"])]}
    
    # otherwise assume parsed is a Pydantic model (CandidateDetails) or dict of parsed fields
    # Build a short acknowledgement message and return parsed result in state so downstream nodes can use it
    # Try to safely extract job_role for a helpful reply
    job_role = ""
    try:
        job_role = getattr(parsed, "job_role", "") or parsed.get("job_role", "")
    except Exception:
        job_role = ""
    
    ack_text = "Resume parsed successfully."
    if job_role:
        ack_text += f" Suggested role(s): {job_role}."
    
    return {
        "messages": [AIMessage(ack_text)],
        "resume_parsed": parsed
    }


class Chatbot:
    def __init__(self, model_name: str):
        self.model_name=model_name
        self.llm=ChatOpenAI(model=self.model_name).bind_tools(tools=TOOLS)
        self.config = None
        self._compiled_graph=None
        self.checkpointer=None
    
    def chat_node(self, state: ChatState):
        messages = state['messages']
        response = self.llm.invoke(messages)
        return {"messages": [response]}

    # Checkpointer
    def build_graph(self, _sqlite=False):
        graph = StateGraph(ChatState)

        graph.add_node("chat_node", self.chat_node)
        graph.add_node("get_resume_details", get_resume_details_node)
        graph.add_node("tools", TOOL_NODE)

        graph.add_edge(START, "get_resume_details")
        graph.add_edge("get_resume_details", "chat_node")

        graph.add_conditional_edges("chat_node", tools_condition)
        graph.add_edge("tools", "chat_node")

        graph.add_edge("chat_node", END)

        if _sqlite:
            conn=sqlite3.connect(database="db/chatbot.db", check_same_thread=False)
            # sqlite_checkpointer=SqliteSaver(conn=conn)
            self.checkpointer=SqliteSaver(conn=conn)
            self._compiled_graph=graph.compile(checkpointer=self.checkpointer)
            self.is_persistent_storage=True
            return self

        self.checkpointer=InMemorySaver()
        self._compiled_graph = graph.compile(checkpointer=self.checkpointer)
        return self
    
    def stream(self, user_message: str, thread_id: str):
        if not self._compiled_graph:
            raise RuntimeError("Graph not built. Call .build_graph() first.")

        self.config={
            "configurable": {
                "thread_id": thread_id
            },
            "metadata": {
                "thread_id": thread_id
            },
            "run_name": "chat_turn"
        }
        stream_generator=self._compiled_graph.stream(
            {"messages": [HumanMessage(user_message)]},
            config=self.config,
            stream_mode="messages"
        )

        # for message_chunk, metadata in stream_generator:
        #     if isinstance(message_chunk, AIMessage):
        #         if hasattr(message_chunk, "content"):
        #             yield message_chunk.content

        full_response=""
        for message_chunk, metadata in stream_generator:
            if isinstance(message_chunk, AIMessage) and hasattr(message_chunk, "content"):
                content_piece = message_chunk.content
                full_response += content_piece  # append to buffer
                yield content_piece  # still stream out in real-time

        # Once stream finishes, log the entire response
        chat_logger.info(
            f"Thread: {thread_id}\nUser: {user_message}\nResponse: {full_response}\n{'-'*80}"
        )

    def chat_history(self, thread_id: str):
        self.config={
            "configurable": {
                "thread_id": thread_id
            }
        }
        history=self._compiled_graph.get_state(config=self.config).values
        messages = history.get("messages", [])

        # Convert each BaseMessage into a dict
        serialized_messages = []
        for msg in messages:
            serialized_messages.append({
                "type": msg.type,    # "human", "ai", "system"
                "content": msg.content
            })

        return {"messages": serialized_messages}
    
    def get_chat_threads(self):
        if not self.is_persistent_storage:
            raise RuntimeError("Object of class Chatbot not built with _sqlite = True.")
        
        all_threads=set()

        for checkpoint in self.checkpointer.list(None):
            all_threads.add(checkpoint.config["configurable"]["thread_id"])

        return list(all_threads)
        