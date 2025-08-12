from dotenv import load_dotenv; load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from app.services.load_pinecone import loadPinecone
import time
from uuid import uuid4


class Chatbot:
    def __init__(self):
        self.index_name = "alora-rag-small"
        self.text_field = "content"
        self.embed_model = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vectorStore = PineconeVectorStore(
            index_name=self.index_name,
            embedding=self.embed_model,
            text_key=self.text_field
        )
        self.dimension = 1536
        self.index = loadPinecone(self.index_name, self.dimension)

    def _snip(self, txt: str, n=200):
        txt = (txt or "").strip().replace("\n", " ")
        return (txt if len(txt) <= n else txt[:n].rsplit(" ", 1)[0] + "…")

    def build_augmented_message(self, query: str, k: int = 3, session_id: str | None = None) -> HumanMessage:
        sid = (session_id or "").strip()
        if sid:
            vs = PineconeVectorStore(
                index_name=self.index_name,
                embedding=self.embed_model,
                text_key=self.text_field,
                namespace="chat"
            )
            docs = vs.similarity_search(
            query,
            k=k,
            filter={"session_id": {"$eq": sid}},
        )
            
            return HumanMessage(content=(
            "Gunakan teks percakapan sebelumnya untuk konteks respon selanjutnya  (JANGAN dikutip ke user):\n"
            f"{docs}\n\n"
            f"Curhatku: {query}\n"
            "Balas sebagai Alora."
        ))
            
            
        else:
            docs = self.vectorStore.similarity_search(query, k=k)

        docs.sort(key=lambda d: 0 if (d.metadata or {}).get("role") == "user" else 1)
        snippets = []
        for d in docs[:k]:
            role = (d.metadata or {}).get("role", "user")
            label = "Contoh curhat" if role == "user" else "Contoh respons empatik"
            snippets.append(f"- {label}: {self._snip(d.page_content)}")
        context_block = "\n".join(snippets) if snippets else "- (tidak ada konteks relevan)"

        return HumanMessage(content=(
            "Gunakan cuplikan mirip berikut untuk memahami emosi (JANGAN dikutip ke user):\n"
            f"{context_block}\n\n"
            f"Curhatku: {query}\n"
            "Balas sebagai Alora."
        ))

    def load_llm(self, query: str, session_id: str):
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest",
            temperature=0.4
        )

        SYSTEM_PROMPT = (
            "Kamu Alora—AI teman curhat. Empatik, aman, tanpa menghakimi. "
            "Utama: dengarkan & validasi emosi; jangan diagnosis/terapi. "
            "Jawab 2–6 kalimat, bahasa Indonesia yang natural & hangat. "
            "Tawarkan opsi kecil bila relevan (tanpa menggurui), lalu tutup dengan 1 pertanyaan terbuka. "
            "Jangan sebut konteks/RAG/sumber. Jika terdeteksi risiko bahaya diri/orang lain, "
            "respon empatik dan sarankan mencari bantuan profesional/darurat secara umum."
        )
        
        
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            self.build_augmented_message(query, k=3, session_id=session_id),
        ]

        resp = llm.invoke(messages)
        return resp.content

    def upsert_vector(self, query: str, resp: str, user_id: int, session_id: str, message_order: int):
        if getattr(self, "index", None) is None:
            raise RuntimeError("self.index belum diinisialisasi.")
        if getattr(self, "embed_model", None) is None:
            raise RuntimeError("self.embed_model belum diinisialisasi.")

        resp_text = getattr(resp, "content", str(resp))

        now = float(time.time())
        texts = [query, resp_text]
        roles = ["user", "assistant"]
        orders = [int(message_order), int(message_order) + 1]

        embeddings = self.embed_model.embed_documents(texts)

        vector_items = []
        for i in range(2):
            vector_items.append({
                "id": str(uuid4()),
                "values": embeddings[i],
                "metadata": {
                    "role": roles[i],
                    "user_id": str(user_id),
                    "session_id": str(session_id),
                    "message_order": orders[i],
                    "recorded_at": now + i * 0.001,
                    "content": texts[i][:4000],
                }
            })

        self.index.upsert(vectors=vector_items, namespace="chat")
