from fastapi import APIRouter
from app.services.chatbot import Chatbot
from pydantic import BaseModel

router = APIRouter()
chatbot = Chatbot()

class TextInput(BaseModel):
    prompt: str
    # user_id: int
    
    
    
@router.post("/alora")
def alora_chatbot(input: TextInput):
    response = chatbot.load_llm(input.prompt)
    return {"response" : response}


