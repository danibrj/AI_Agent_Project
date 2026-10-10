from fastapi import APIRouter
from Backend.models.models import ChatRequest, ChatResponse
from Backend.AI_agent.agent import run_agent
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from Database.database import get_db

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    
    response = await run_agent(request.conversation_id,request.text, db)
    
    return {
        "response": response
    }