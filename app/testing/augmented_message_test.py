# test_augmented_message.py
from dotenv import load_dotenv; load_dotenv()
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.schema import HumanMessage

INDEX_NAME = "alora-rag-small"
TEXT_FIELD = "content"
EMBED_MODEL = "text-embedding-3-small"

SESSION_ID = "a1b30d41-385e-414f-88af-e89c90079440"  
QUERY = "aku lagi cemas soal besok ketemu dosen pembimbing, takut dimarahin"
K = 3

def _snip(txt: str, n: int = 200) -> str:
    txt = (txt or "").strip().replace("\n", " ")
    return txt if len(txt) <= n else txt[:n].rsplit(" ", 1)[0] + "…"

def build_augmented_message(query: str, k: int = 3, session_id: str | None = None) -> HumanMessage:
    sid = (session_id or "").strip()
    print(f"[TEST] session_id(normalized)='{sid}'")

    embed_model = OpenAIEmbeddings(model=EMBED_MODEL)

    if sid:
        print(f"[RAG] MODE=CHAT ns='chat'")
        vs = PineconeVectorStore(
            index_name=INDEX_NAME,
            embedding=embed_model,
            text_key=TEXT_FIELD,
            namespace="chat"
        )
        filter_condition = {"session_id": sid}

        docs = vs.similarity_search(
            query,
            k=k * 4,               
            filter=filter_condition,
            namespace="chat"
            
        )
        print(f"[RAG] Found {len(docs)} docs for session_id={sid}")

        if not docs:
            print("[RAG] 0 hasil. Cek lagi: SID tepat? namespace='chat'? metadata key 'session_id'?")
            return HumanMessage(content=(
                "Gunakan percakapan sebelumnya untuk konteks (JANGAN dikutip ke user):\n"
                "- (tidak ada konteks relevan)\n\n"
                f"Curhatku: {query}\n"
                "Balas sebagai Alora."
            ))

        docs_sorted = sorted(docs, key=lambda d: float((d.metadata or {}).get("message_order", 0.0)))
        recent_docs = docs_sorted[-k:]

        print(f"[RAG] Using last {len(recent_docs)} by message_order:")
        for i, d in enumerate(recent_docs, 1):
            md = d.metadata or {}
            print(f"  {i}. order={md.get('message_order')} role={md.get('role')} sid={md.get('session_id')}")
            print(f"     {_snip(d.page_content, 120)}")

        parts = []
        for d in recent_docs:
            role = (d.metadata or {}).get("role", "user")
            speaker = "User" if role == "user" else "Alora"
            parts.append(f"{speaker}: {d.page_content.strip()}")

        context_block = "\n".join(parts)

        return HumanMessage(content=(
            "Gunakan percakapan sebelumnya untuk konteks (JANGAN dikutip ke user):\n"
            f"{context_block}\n\n"
            f"Curhatku: {query}\n"
            "Balas sebagai Alora."
        ))

    print("[RAG] MODE=SEED (default namespace)")
    vs = PineconeVectorStore(
        index_name=INDEX_NAME,
        embedding=embed_model,
        text_key=TEXT_FIELD
    )
    docs = vs.similarity_search(query, k=k)
    print(f"[RAG] SEED found {len(docs)} docs")

    docs.sort(key=lambda d: 0 if (d.metadata or {}).get("role") == "user" else 1)
    snippets = []
    for d in docs[:k]:
        role = (d.metadata or {}).get("role", "user")
        label = "Contoh curhat" if role == "user" else "Contoh respons empatik"
        snippets.append(f"- {label}: {_snip(d.page_content)}")
    context_block = "\n".join(snippets) if snippets else "- (tidak ada konteks relevan)"

    return HumanMessage(content=(
        "Gunakan cuplikan mirip berikut untuk memahami emosi (JANGAN dikutip ke user):\n"
        f"{context_block}\n\n"
        f"Curhatku: {query}\n"
        "Balas sebagai Alora."
    ))

if __name__ == "__main__":
    msg = build_augmented_message(QUERY, k=K, session_id=SESSION_ID)
    print("\n==== [AUGMENTED MESSAGE] ====\n")
    print(msg.content)
