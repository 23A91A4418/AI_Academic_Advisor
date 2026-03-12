from .database import SessionLocal
from .models import ConversationModel, UserPreferencesModel, MilestoneModel
from .memory_schemas import Conversation, UserPreferences, Milestone
from .vector_store import add_memory_embedding


def memory_write(memory_type: str, data: dict):

    db = SessionLocal()

    if memory_type == "conversation":

        memory = Conversation(**data)

        db_obj = ConversationModel(
            user_id=memory.user_id,
            turn_id=memory.turn_id,
            role=memory.role,
            content=memory.content,
            timestamp=memory.timestamp
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        add_memory_embedding(
            memory_id=str(db_obj.id),
            text=memory.content,
            metadata={"user_id": memory.user_id, "type": "conversation"}
        )

        return {"status": "success", "memory_id": db_obj.id}

    elif memory_type == "preference":

        memory = UserPreferences(**data)

        db_obj = UserPreferencesModel(
            user_id=memory.user_id,
            preferences=memory.preferences
        )

        db.add(db_obj)
        db.commit()

        return {"status": "success"}

    elif memory_type == "milestone":

        memory = Milestone(**data)

        db_obj = MilestoneModel(
            user_id=memory.user_id,
            milestone_id=memory.milestone_id,
            description=memory.description,
            status=memory.status,
            date_achieved=memory.date_achieved
        )

        db.add(db_obj)
        db.commit()

        return {"status": "success"}

    else:
        return {"error": "Invalid memory type"}
def memory_read(user_id: str, query_type: str, params: dict):

    db = SessionLocal()

    if query_type == "last_n_turns":

        n = params.get("n", 5)

        results = (
            db.query(ConversationModel)
            .filter(ConversationModel.user_id == user_id)
            .order_by(ConversationModel.timestamp.desc())
            .limit(n)
            .all()
        )

        return {
            "results": [
                {
                    "user_id": r.user_id,
                    "turn_id": r.turn_id,
                    "role": r.role,
                    "content": r.content,
                    "timestamp": r.timestamp
                }
                for r in results
            ]
        }

    return {"error": "Invalid query type"}
from .vector_store import search_memory


def memory_retrieve_by_context(user_id: str, query_text: str, top_k: int = 3):

    results = search_memory(query_text, top_k)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    output = []

    for doc, meta in zip(documents, metadatas):

        if meta.get("user_id") == user_id:

            output.append({
                "content": doc,
                "metadata": meta
            })

    return {"results": output}