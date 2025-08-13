# Emolog Detector & Alora Chatbot

This repository contains **two separate components**

* **Emolog Detector** — emotion classification for Indonesian text based on IndoBERT (label: *Bersyukur, Marah, Sedih, Senang, Stress*).
* **Alora Chatbot** — empathetic Indonesian-language chatbot powered by LLM, enhanced with a **Retrieval-Augmented Generation (RAG)** pipeline.
  * **RAG process**: stores and retrieves relevant conversation history or external knowledge from a vector database, then feeds it into the LLM to maintain context, accuracy, and empathy throughout the conversation.
  * This allows the chatbot to **remember past interactions**, respond consistently, and adapt its tone based on the user’s emotional state.

## Components

### 1) Emolog Detector

* Classifies emotions for single or multiple texts.
* Returns **label** for each label.
* Model: `Atherizz/emolog-indobert` (Hugging Face).

**Emotion Label**

| ID | Label     |
| -- | --------- |
| 0  | Bersyukur |
| 1  | Marah     |
| 2  | Sedih     |
| 3  | Senang    |
| 4  | Stress    |

### 2) Alora Chatbot

* Empathetic & natural Indonesian-language chatbot.
* Can run purely using LLM (without Emolog).
* Utilizes memory/RAG for conversation context.
* Response principles: validate feelings, use neutral and safe language.

---

## Installation

```bash
git clone https://github.com/username/emolog-detector.git
cd emolog-detector

python -m venv venv
# Windows PowerShell
. .\venv\Scripts\Activate.ps1
# macOS/Linux
source .env/bin/activate

pip install -r requirements.txt
