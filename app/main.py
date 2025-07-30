from fastapi import FastAPI
from pydantic import BaseModel
from app.detector import EmologDetector

app = FastAPI(title="Emolog API")

detector = EmologDetector()

class TextInput(BaseModel):
    text: str
    return_all_scores: bool = False

@app.post("/predict")
def predict_emotion(input: TextInput):
    result = detector.predict_emotion(input.text, input.return_all_scores)
    return {"perasaan kamu saat ini": result}
