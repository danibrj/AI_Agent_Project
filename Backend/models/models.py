from pydantic import BaseModel

class ChatRequest(BaseModel):
    conversation_id: int
    text: str


class ChatResponse(BaseModel):
    response: str