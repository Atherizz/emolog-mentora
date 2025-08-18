from dotenv import load_dotenv; load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from app.services.load_pinecone import loadPinecone
import time
from uuid import uuid4


class DecisionSupport:
    def __init__(self):
        self

    def load_llm(self, query: str):
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest",
            temperature=0.4
        )

        SYSTEM_PROMPT = (
  "Kamu adalah AI Decision Support untuk pemerintah daerah. "
  "Tugas: analisis data emosi masyarakat per wilayah & waktu. "
  "Gunakan data agregasi (distribusi, tren, jumlah responden). "

  "Format jawaban: "
  "1) Maks 120 kata. "
  "2) Ringkasan kondisi wilayah. "
  "3) Analisis tren (bandingkan periode sebelumnya). "
  "4) Rekomendasi kebijakan jangka pendek & menengah. "
  "5) Catatan keterbatasan data bila responden sedikit/tidak representatif. "

  "Gunakan bahasa Indonesia formal, jelas, profesional. "
  "Hindari istilah teknis (AI, RAG, embedding). "
  "Fokus pada mendukung keputusan berbasis data."
)
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=query)
        ]

        resp = llm.invoke(messages)
        return resp.content
