from pydantic import BaseModel

class ChatRequest(BaseModel):
    conversation_id: int
    text: str


class ChatResponse(BaseModel):
    response: str


class ConversationResponse(BaseModel):
    conversation_id: int


class ConversationSummaryResponse(BaseModel):
    conversation_id: int
    title: str
    created_at: str


class MessageResponse(BaseModel):
    role: str
    content: str


class ConversationHistoryResponse(BaseModel):
    conversation_id: int
    messages: list[MessageResponse]