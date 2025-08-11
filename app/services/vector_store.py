import os
import time
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from datasets import load_dataset
from load_pinecone import loadPinecone

load_dotenv()
pineconeApiKey = os.getenv("PINECONE_API_KEY")
openAIApiKey = os.getenv("OPENAI_API_KEY")

dataset = load_dataset("IzzulGod/indonesian-conversation", split="train")

index_name = "alora-rag-small"
model_name = "text-embedding-3-small"
dimension = 1536

pc = Pinecone(api_key=pineconeApiKey)

index = loadPinecone(index_name, dimension)

desc = pc.describe_index(index_name)
print(desc.status)
print(f"Index '{index_name}' siap digunakan 🚀")
print(index.describe_index_stats())

embed_model = OpenAIEmbeddings(model=model_name)

batch_size = 100
batch_texts, batch_ids, batch_metadatas = [], [], []

for i, row in enumerate(dataset):
    messages = row["messages"]
    for j, msg in enumerate(messages):
        content = msg.get("content", "")
        if not content:
            continue

        batch_ids.append(f"conv{i}_msg{j}")
        batch_texts.append(content)
        batch_metadatas.append(
            {
                "role": msg.get("role", ""),
                "conversation_id": i,
                "message_order": j,
                "content" : content[:4000].strip()
            }
        )

        if len(batch_texts) >= batch_size:
            embeds = embed_model.embed_documents(batch_texts)
            index.upsert(vectors=list(zip(batch_ids, embeds, batch_metadatas)))
            batch_texts, batch_ids, batch_metadatas = [], [], []

if batch_texts:
    embeds = embed_model.embed_documents(batch_texts)
    index.upsert(vectors=list(zip(batch_ids, embeds, batch_metadatas)))

# texts = [
#     "this is the first chunk of text",
#     "then another second chunk of text is here",
# ]
# res = embed_model.embed_documents(texts)
# print(len(res))
# print(len(res[0]))  
