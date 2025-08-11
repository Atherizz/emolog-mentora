import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np

class EmologDetector:
    def __init__(self, model_path="Atherizz/emolog-indobert"):
        """
        Inisialisasi detector emosi
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        print(f"🔄 Memuat model dari {model_path}...")
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        
        self.id2label = {
            0: 'Bersyukur',
            1: 'Marah', 
            2: 'Sedih',
            3: 'Senang',
            4: 'Stress'
        }
        
        self.model.eval()
        print("✅ Model berhasil dimuat!")
    
    def predict_emotion(self, text, return_all_scores=False):
        """
        Prediksi emosi dari teks
        
        Args:
            text (str): Teks yang akan diprediksi
            return_all_scores (bool): Jika True, return semua skor emosi
            
        Returns:
            dict: Hasil prediksi
        """
        # Tokenization
        inputs = self.tokenizer(
            text, 
            return_tensors="pt", 
            truncation=True, 
            padding=True,
            max_length=128
        )
        
        # Prediction
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        # Konversi ke numpy
        scores = predictions.cpu().numpy()[0]
        
        # Ambil prediksi terbaik
        predicted_id = np.argmax(scores)
        predicted_label = self.id2label[predicted_id]
        
        result = predicted_label
        
        if return_all_scores:
            all_scores = {self.id2label[i]: float(score) for i, score in enumerate(scores)}
            result['all_scores'] = all_scores
            
        return result
    
    def predict_batch(self, texts):
        """
        Prediksi batch teks sekaligus
        """
        results = []
        for text in texts:
            result = self.predict_emotion(text)
            results.append(result)
        return results

