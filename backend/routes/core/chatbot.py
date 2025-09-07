from fastapi import (
    FastAPI,
    HTTPException,
    APIRouter,
    Depends,
    Request,
    Query
)
from fastapi.responses import JSONResponse, StreamingResponse
from schema import (
    user,
    user_profile
)
from db.models.orm_funcs import (
    SessionLocal,
    Users,
    UserProfile,
    get_db
)
import core.jwt_config as security
from sqlalchemy.orm import Session
from core.logger_config import get_logger
from core.auth_dependency import get_current_user
from schema.chatbot_models import ChatInput
from utils import stream_json

from services.workflows.agent_model import Chatbot

logger=get_logger("login")

bot_route=APIRouter(prefix="/core")

@bot_route.post("/get-response")
def get_response(payload: ChatInput, user: str = Depends(get_current_user)) -> dict:
    message = payload.message
    thread_id = payload.thread_id

    return StreamingResponse(
        content=stream_json(message=message, thread_id=thread_id),
        media_type="application/x-ndjson"
    )


@bot_route.get("/chat-history")
def get_chat_history(thread_id: str = Query(...), user: str = Depends(get_current_user)) -> dict:
    bot = Chatbot(model_name="gpt-4o").build_graph(_sqlite=True)
    history=bot.chat_history(thread_id=thread_id)

    return JSONResponse(status_code=200, content=history)


@bot_route.get("/all_threads")
def get_threads():
    bot=Chatbot(model_name="gpt-4o").build_graph(_sqlite=True)
    threads=bot.get_chat_threads()

    return JSONResponse(status_code=200, content={"response": threads})