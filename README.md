

# 🧠 Emolog Detector - Klasifikasi Emosi Bahasa Indonesia

Deteksi emosi dari teks Bahasa Indonesia menggunakan model IndoBERT yang sudah di-finetune. Model ini dapat mengenali emosi seperti **Bersyukur**, **Marah**, **Sedih**, **Senang**, dan **Stress**. Cocok buat riset NLP, sistem monitoring kesehatan mental, atau chatbot yang lebih manusiawi 😌.

---

## 📦 Fitur Utama

- 🔍 Deteksi satu teks (single prediction)
- 🧪 Batch prediction (multi-text)
- 📊 Skor probabilitas untuk semua label emosi
- 🧠 Menggunakan IndoBERT yang sudah di-finetune
- 🗣️ Model Bahasa Indonesia

---

## 🛠️ Instalasi

### 1. Clone Repository *(kalau belum)*
```bash
git clone https://github.com/username/emolog-detector.git
cd emolog-detector
````

```bash
python -m venv .env
# Aktifkan (Windows PowerShell)
.env\Scripts\Activate.ps1
# atau (Command Prompt)
.env\Scripts\activate.bat
# atau (macOS/Linux)
source .env/bin/activate
```

### 3. Install Dependencies

```bash
pip install torch transformers numpy
```

---

## 🚀 Menjalankan Program

Jalankan file utama:

```bash
python emolog_test.py
```

Kamu akan masuk ke mode interaktif:

```
🎯 TESTING MODEL EMOLOG DETECTOR
🔄 Mode Interaktif - Ketik 'quit' untuk keluar

Masukkan teks: aku merasa capek dan tidak berguna
🎯 Emosi: Sedih (0.942)
📊 Semua skor:
   Bersyukur : 0.002
   Marah     : 0.005
   Sedih     : 0.942
   Senang    : 0.010
   Stress    : 0.041
```

---

## 🧠 Cara Kerja

1. Teks dimasukkan oleh pengguna.
2. Tokenizer mengubah teks menjadi input tensor.
3. Model memproses input menggunakan IndoBERT yang sudah di-finetune.
4. Output berupa skor probabilitas untuk tiap label emosi.
5. Skor tertinggi diambil sebagai label prediksi.

---

## 🧬 Label Emosi

| ID | Label     |
| -- | --------- |
| 0  | Bersyukur |
| 1  | Marah     |
| 2  | Sedih     |
| 3  | Senang    |
| 4  | Stress    |

---

## 🗂️ Struktur Folder

```
emolog-test-project/
├── emolog_test.py         # Script utama
├── README.md              # Dokumentasi ini
├── .env/                  # Virtual environment (opsional)
```

---

## 🌐 Model

Model yang digunakan:
📦 [Atherizz/emolog-indobert](https://huggingface.co/Atherizz/emolog-indobert)

---


