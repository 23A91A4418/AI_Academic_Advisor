import os
import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")

client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

collection = client.get_or_create_collection(
    name="advisor_memory"
)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
def add_memory_embedding(memory_id: str, text: str, metadata: dict):
    
    embedding = embedding_model.encode(text).tolist()

    collection.add(
        ids=[memory_id],
        embeddings=[embedding],
        documents=[text],
        metadatas=[metadata]
    )
def search_memory(query_text: str, top_k: int = 3):

    query_embedding = embedding_model.encode(query_text).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results