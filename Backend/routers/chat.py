from fastapi import APIRouter
from models.models import ChatRequest, ChatResponse
from AI_agent.agent import run_agent

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    
    response = await run_agent(request.text)
    
    return {
        "response": response
    }