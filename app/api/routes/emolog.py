from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.core.security import verify_jwt
from app.db.models.emolog_histories import EmologHistories, InsertHistory, GetHistoryByUserId
from app.services.detector import EmologDetector
from datetime import datetime
from pydantic import BaseModel
from fastapi.responses import JSONResponse

router = APIRouter()
detector = EmologDetector()

class TextInput(BaseModel):
    text: str
    return_all_scores: bool = False

@router.post("/predict")
def predict_emotion(input: TextInput, user_data: dict = Depends(verify_jwt),session: Session = Depends(get_session)):
    result = detector.predict_emotion(input.text, input.return_all_scores)

    history = EmologHistories(
        user_id=user_data.id, 
        emotion_label=result,
        text_input=input.text,
        subdistrict_id=1,
        recorded_at=datetime.utcnow()
    )

    InsertHistory(history, session)

    return {"perasaan kamu saat ini": result}

@router.get("/emolog-history")
def get_emolog_history(user_data: dict = Depends(verify_jwt), session: Session = Depends(get_session)):
    histories = GetHistoryByUserId(user_data.id, session)
    
    return histories