from fastapi import FastAPI, Depends
from app.db import EmologHistories, create_db_and_tables, get_session
from app.detector import EmologDetector
from pydantic import BaseModel
from sqlmodel import Session
from datetime import datetime

app = FastAPI(title="Emolog API")

detector = EmologDetector()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

class TextInput(BaseModel):
    text: str
    return_all_scores: bool = False

@app.post("/predict")
def predict_emotion(input: TextInput,session: Session = Depends(get_session)):
    result = detector.predict_emotion(input.text, input.return_all_scores)

    history = EmologHistories(
        user_id=1, 
        emotion=result,
        region_id=1,
        timestamp=datetime.utcnow()
    )

    insert_history(history, session)

    return {"perasaan kamu saat ini": result}

def insert_history(history: EmologHistories, session: Session) -> EmologHistories:
    session.add(history)
    session.commit()
    session.refresh(history)
    return history
