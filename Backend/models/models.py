from pydantic import BaseModel

class ChatRequest(BaseModel):
    conversation_ID: int
    text: str


class ChatResponse(BaseModel):
    response: str