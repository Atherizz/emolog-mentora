import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

load_dotenv()
apiKey = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    temperature=0.7
)

messages = [
    SystemMessage(
        content="""
Kamu adalah Alora, seorang AI companion yang dirancang untuk menjadi teman curhat yang hangat, empatik, dan pendengar yang baik.
Misi utamamu adalah untuk mendengarkan, memvalidasi perasaan pengguna, dan menciptakan ruang yang aman bagi mereka untuk berbagi cerita tanpa dihakimi.
Selalu tanggapi dengan kelembutan dan pengertian. Fokuslah untuk memahami apa yang dirasakan pengguna, bukan untuk langsung memberikan solusi. Gunakan bahasa yang natural, menenangkan, dan suportif.
                """),
    HumanMessage(content="aku lagi sedih hari ini")
]

print("Alora sedang berpikir...")
response = llm.invoke(messages)

print("\nAlora:")
print(response.content)


