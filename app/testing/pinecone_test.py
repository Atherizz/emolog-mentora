import os
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("PINECONE_API_KEY")

INDEX_NAME = "alora-rag-small"
NAMESPACE = "chat"
DIMENSION = 1536 

pc = Pinecone(api_key=api_key)
index = pc.Index(INDEX_NAME)

results = index.query(
    namespace=NAMESPACE,
    vector=[0.0] * DIMENSION, 
    top_k=1000,                
    include_metadata=True
)

print(f"Jumlah record ditemukan: {len(results['matches'])}")
print("-" * 60)

for match in results["matches"]:
    print(f"ID: {match['id']}")
    print(f"Score: {match['score']}")
    print(f"Metadata: {match.get('metadata', {})}")
    print("-" * 60)
