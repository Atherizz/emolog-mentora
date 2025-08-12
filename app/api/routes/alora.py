from fastapi import APIRouter
from app.services.chatbot import Chatbot
from pydantic import BaseModel

router = APIRouter()
chatbot = Chatbot()

class ChatRequest(BaseModel):
    prompt: str
    session_id: str

class UpsertRequest(BaseModel):
    prompt: str
    resp: str
    user_id: int
    session_id: str
    message_order: int
    
@router.post("/alora")
def alora_chatbot(input: ChatRequest):
    response = chatbot.load_llm(input.prompt, input.session_id)
    return {"message" : response}

@router.post("/upsert-vector")
def upsert_vector(input: UpsertRequest):
    chatbot.upsert_vector(input.prompt, input.resp, input.user_id, input.session_id, input.message_order)


