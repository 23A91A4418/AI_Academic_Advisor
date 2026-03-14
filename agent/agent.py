import requests

MCP_URL = "http://mcp_server:8000"


def retrieve_memory(user_id, query):
    response = requests.post(
        f"{MCP_URL}/invoke/memory_retrieve_by_context",
        json={
            "user_id": user_id,
            "query_text": query,
            "top_k": 1
        }
    )

    data = response.json()
    results = data.get("results", [])

    if results:
        return results[0]["content"]

    return None


def store_memory(user_id, turn_id, role, content):
    requests.post(
        f"{MCP_URL}/invoke/memory_write",
        json={
            "memory_type": "conversation",
            "data": {
                "user_id": user_id,
                "turn_id": turn_id,
                "role": role,
                "content": content
            }
        }
    )


def run_agent():

    user_id = "student_01"
    turn_id = 1

    while True:

        user_input = input("User: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        # Retrieve memory
        results = requests.post(
            f"{MCP_URL}/invoke/memory_retrieve_by_context",
            json={
                "user_id": user_id,
                "query_text": user_input,
                "top_k": 5
            }
        ).json().get("results", [])

        # Filter out current message if it matches exactly
        memory_content = None
        for res in results:
            content = res.get("content", "")
            role = res.get("metadata", {}).get("role")
            
            if content.lower() == user_input.lower():
                continue
                
            if role == "assistant" or "I remember you mentioned:" in content:
                continue
                
            memory_content = content
            break

        if memory_content:
            print(f"\n[DEBUG] Found relevant memory: {memory_content}")
            response = f"I remember you mentioned: \"{memory_content}\". Based on that, I recommend exploring specialized courses and projects in that area."
        else:
            response = "I'm here to help with your academic planning. What subjects or goals are you interested in?"

        print("Advisor:", response)

        # Store useful user messages
        if "earlier" not in user_input.lower():
            store_memory(user_id, turn_id, "user", user_input)

        # Store assistant response
        store_memory(user_id, turn_id, "assistant", response)

        turn_id += 1


if __name__ == "__main__":
    run_agent()