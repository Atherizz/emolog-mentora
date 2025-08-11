from dotenv import load_dotenv; load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings

class Chatbot:
    def __init__(self):
        self.index_name = "alora-rag-small"
        self.text_field = "content"
        self.embed_model = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vectorStore = PineconeVectorStore(index_name=self.index_name, embedding=self.embed_model, text_key=self.text_field)
        
    def _snip(self, txt: str, n=200):
        txt = (txt or "").strip().replace("\n", " ")
        return (txt if len(txt) <= n else txt[:n].rsplit(" ", 1)[0] + "…")
    
    def build_augmented_message(self,query: str, k: int = 3) -> HumanMessage:
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
        
    def load_llm(self, query: str):
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.4)
        
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
        self.build_augmented_message(query, k=3),
        ]

        resp = llm.invoke(messages)
        return resp.content
    
    def upsertRecord(self, user_id: int, query: str):
        embeds = self.embed_model.embed_documents(query)

        

        




