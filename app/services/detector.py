import os, threading
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class EmologDetector:
    def __init__(self, model_path="Atherizz/emolog-indobert"):
        print(f"🔄 Memuat model dari {model_path}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=True)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_path,
            torch_dtype="auto" if torch.cuda.is_available() else None
        )
        self.model.eval()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

        self.id2label = {
            0: 'Bersyukur',
            1: 'Marah',
            2: 'Sedih',
            3: 'Senang',
            4: 'Stress'
        }
        print("✅ Model berhasil dimuat!")

    def predict_emotion(self, text: str, return_all_scores: bool = False):
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=-1)[0].cpu().numpy()

        idx = int(np.argmax(probs))
        label = self.id2label[idx]

        if return_all_scores:
            return {
                "label": label,
                "scores": {self.id2label[i]: float(s) for i, s in enumerate(probs)}
            }
        return {"label": label}

_detector = None
_lock = threading.Lock()

def get_detector() -> EmologDetector:
    global _detector
    if _detector is None:
        with _lock:
            if _detector is None:
                _detector = EmologDetector()
    return _detector
