from fastapi import APIRouter, Depends
from app.services.decision_support import DecisionSupport
from datetime import datetime
from pydantic import BaseModel
from fastapi.responses import JSONResponse

router = APIRouter()
decision_support = DecisionSupport()

class TextInput(BaseModel):
    prompt: str

@router.post("/analyze")
def predict_emotion(input: TextInput):
    result = decision_support.load_llm(input.prompt)
    return {"insights": result}
