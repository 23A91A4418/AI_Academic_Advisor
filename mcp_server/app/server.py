from fastapi import FastAPI
from .database import engine
from .models import Base
from fastapi import FastAPI
from .tools import memory_write, memory_read, memory_retrieve_by_context

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/tools")
def list_tools():
    return {
        "tools": [
            {"name": "memory_write", "description": "Store memory"},
            {"name": "memory_read", "description": "Retrieve structured memory"},
            {"name": "memory_retrieve_by_context", "description": "Semantic search"}
        ]
    }
@app.post("/invoke/memory_write")
def invoke_memory_write(payload: dict):

    return memory_write(
        memory_type=payload["memory_type"],
        data=payload["data"]
    )


@app.post("/invoke/memory_read")
def invoke_memory_read(payload: dict):

    return memory_read(
        user_id=payload["user_id"],
        query_type=payload["query_type"],
        params=payload.get("params", {})
    )


@app.post("/invoke/memory_retrieve_by_context")
def invoke_memory_retrieve(payload: dict):

    return memory_retrieve_by_context(
        user_id=payload["user_id"],
        query_text=payload["query_text"],
        top_k=payload.get("top_k", 3)
    )