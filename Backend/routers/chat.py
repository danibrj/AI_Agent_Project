from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from Backend.AI_agent.agent import run_agent
from sqlalchemy.orm import Session
from Database.database import get_db
from Database.models import Conversation, Message
from Backend.models.models import (
    ChatRequest,
    ChatResponse,
    ConversationHistoryResponse,
    ConversationResponse,
    ConversationSummaryResponse,
)


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/conversations", response_model=ConversationResponse, status_code=201)
def create_conversation(db: Session = Depends(get_db)):
    conversation = Conversation(created_at=str(datetime.now()))
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return {"conversation_id": conversation.id}


@router.get(
    "/conversations",
    response_model=list[ConversationSummaryResponse],
)
def list_conversations(db: Session = Depends(get_db)):
    first_user_message = (
        select(Message.content)
        .where(
            Message.conversation_id == Conversation.id,
            Message.role == "user",
        )
        .order_by(Message.id)
        .limit(1)
        .scalar_subquery()
    )
    conversations = (
        db.query(Conversation, first_user_message.label("title"))
        .order_by(Conversation.id.desc())
        .all()
    )

    summaries = []
    for conversation, title in conversations:
        title = (title or "").strip() or "گفتگوی جدید"
        if len(title) > 60:
            title = f"{title[:60].rstrip()}…"
        summaries.append(
            {
                "conversation_id": conversation.id,
                "title": title,
                "created_at": conversation.created_at or "",
            }
        )
    return summaries


@router.get(
    "/conversations/{conversation_id}",
    response_model=ConversationHistoryResponse,
)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )
    if conversation is None:
        raise HTTPException(status_code=404, detail="گفتگو پیدا نشد.")

    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.id)
        .all()
    )
    return {
        "conversation_id": conversation.id,
        "messages": [
            {"role": message.role, "content": message.content}
            for message in messages
        ],
    }


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    response = await run_agent(request.conversation_id, request.text, db)

    return {
        "response": response
    }