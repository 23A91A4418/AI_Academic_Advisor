import requests

MCP_URL = "http://mcp_server:8000"

USER_ID = "student_001"


def write_memory(turn_id, role, content):

    payload = {
        "memory_type": "conversation",
        "data": {
            "user_id": USER_ID,
            "turn_id": turn_id,
            "role": role,
            "content": content
        }
    }

    requests.post(f"{MCP_URL}/invoke/memory_write", json=payload)


def search_memory(query):

    payload = {
        "user_id": USER_ID,
        "query_text": query,
        "top_k": 3
    }

    response = requests.post(
        f"{MCP_URL}/invoke/memory_retrieve_by_context",
        json=payload
    )

    return response.json()


def advisor_response(user_input):

    memory = search_memory(user_input)

    retrieved_context = ""

    if memory["results"]:
        for item in memory["results"]:
            retrieved_context += item["content"] + "\n"

    response = f"""
Relevant past information:
{retrieved_context}

Advisor Response:
Based on your interests, here is my advice.
"""

    return response


def run_agent():

    turn = 1

    while True:

        user_input = input("User: ")

        if user_input.lower() == "exit":
            break

        write_memory(turn, "user", user_input)

        response = advisor_response(user_input)

        print("Advisor:", response)

        write_memory(turn + 1, "assistant", response)

        turn += 2


if __name__ == "__main__":
    run_agent()