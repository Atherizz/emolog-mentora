# 🧠 Emolog Detector & 🤍 Alora Chatbot 

Repo ini berisi **dua komponen berbeda** yang dapat digunakan **mandiri**:

* **Emolog Detector** — klasifikasi emosi teks Bahasa Indonesia berbasis IndoBERT (label: *Bersyukur, Marah, Sedih, Senang, Stress*).
* **Alora Chatbot** — chatbot empatik berbahasa Indonesia berbasis LLM 


---

## Komponen

### 1) Emolog Detector

* Klasifikasi emosi untuk satu atau banyak teks.
* Mengembalikan **label** dan **skor probabilitas** per label.
* Model: `Atherizz/emolog-indobert` (Hugging Face).

**Label Emosi**

| ID | Label     |
| -- | --------- |
| 0  | Bersyukur |
| 1  | Marah     |
| 2  | Sedih     |
| 3  | Senang    |
| 4  | Stress    |

### 2) Alora Chatbot

* Chatbot empatik & natural berbahasa Indonesia.
* Dapat berjalan murni menggunakan LLM (tanpa Emolog).
* Memanfaatkan memori/RAG untuk konteks percakapan.
* Prinsip respons: validasi perasaan, bahasa netral, dan aman.

---

## Instalasi

```bash
git clone https://github.com/username/emolog-detector.git
cd emolog-detector

python -m venv .env
# Windows PowerShell
. .\venv\Scripts\Activate.ps1
# macOS/Linux
source .env/bin/activate

pip install -r requirements.txt
```

