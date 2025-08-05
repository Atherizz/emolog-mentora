from fastapi import APIRouter, Depends
# from sqlmodel import Session
# from app.db.session import get_session
# from app.core.security import verify_jwt
# from app.db.models.emolog_histories import EmologHistories, InsertHistory, GetHistoryByUserId
from app.services.detector import EmologDetector
from datetime import datetime
from pydantic import BaseModel
from fastapi.responses import JSONResponse

router = APIRouter()
detector = EmologDetector()

class TextInput(BaseModel):
    text: str
    subdistrict_id: int
    return_all_scores: bool = False

@router.post("/predict")
def predict_emotion(input: TextInput):
    result = detector.predict_emotion(input.text, input.return_all_scores)

    return {"emotion_label": result}

