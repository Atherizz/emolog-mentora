import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage

def main():
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError("GOOGLE_API_KEY belum diset di .env")

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest",
        temperature=0.7,
    )
    messages = [
        SystemMessage(content=(
            "Kamu adalah Alora, AI companion yang hangat, empatik, dan pendengar yang baik. "
            "Fokus pada memahami perasaan user, validasi emosi, tidak menghakimi, dan tawarkan dukungan. "
            "Gunakan bahasa Indonesia yang lembut dan natural."
        ))
    ]

    print("Alora siap dengerin. Ketik 'exit' atau 'quit' untuk keluar.\n")

    try:
        while True:
            user_input = input("You : ").strip()
            if not user_input:
                continue
            if user_input.lower() in {"exit", "quit"}:
                print("Alora: Makasih sudah cerita hari ini. Jaga diri baik-baik ya 💛")
                break

            messages.append(HumanMessage(content=user_input))

            print("Alora sedang berpikir...\n")
            ai_msg = llm.invoke(messages)

            print("Alora:", ai_msg.content, "\n")
            messages.append(ai_msg)

    except KeyboardInterrupt:
        print("\nAlora: Sampai ketemu lagi ya. Take care! 🌤️")

if __name__ == "__main__":
    main()
