from pydantic import BaseModel, Field
from typing import Annotated

class ChatInput(BaseModel):
    message: Annotated[str, Field(...,description="Message to send to the chatbot.")]
    thread_id: Annotated[str, Field(..., description="Thread ID of the message.")]