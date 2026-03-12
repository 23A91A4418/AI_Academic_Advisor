# AI Academic Advisor with MCP Memory Architecture

## Overview

This project implements an **AI Academic Advisor Agent** that maintains long-term, context-aware memory using the **Memory-Control-Process (MCP)** architecture. The system overcomes the context limitations of large language models by externalizing memory into persistent storage systems.

The agent can store and retrieve user conversations, preferences, and academic milestones while also performing **semantic memory retrieval** using vector embeddings. This enables personalized and context-aware responses across multiple sessions.

The entire system is fully containerized using Docker and can be launched with a single command.

---

## Key Features

- Persistent AI memory using relational and vector databases
- Semantic memory retrieval using embeddings
- Tool-based architecture enabling LLM agents to interact with memory
- Hybrid memory system (structured + semantic)
- Containerized deployment using Docker
- Scalable modular architecture following MCP principles

---

## MCP Architecture

The system follows the **Memory-Control-Process architecture**, which separates memory management from the AI agent.


User
│
▼
AI Agent (Process Layer)
│
▼
MCP Server (Control Layer)
│
├── SQLite (Structured Memory)
│
└── ChromaDB (Vector Semantic Memory)


### Components

**User**
- Interacts with the AI advisor through conversational queries.

**AI Agent (Process Layer)**
- Processes user queries
- Determines when memory access is required
- Calls MCP tools to read or write memory

**MCP Server (Control Layer)**
- Provides API endpoints for memory operations
- Validates memory objects using Pydantic schemas
- Coordinates interactions between the agent and memory databases

**Structured Memory (SQLite)**
- Stores structured data such as conversation history, preferences, and milestones.

**Vector Memory (ChromaDB)**
- Stores embeddings of text memories for semantic search and context retrieval.

---

## System Architecture Diagram

            ┌───────────────────────────┐
            │           User            │
            └───────────────┬───────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │        AI Agent           │
            │      (Advisor Logic)      │
            └───────────────┬───────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │        MCP Server         │
            │      FastAPI Backend      │
            │                           │
            │  Tools:                   │
            │  • memory_write           │
            │  • memory_read            │
            │  • memory_retrieve_by_context │
            └───────────┬───────────┬───┘
                        │           │
                        ▼           ▼
              ┌─────────────────┐ ┌─────────────────┐
              │     SQLite      │ │    ChromaDB     │
              │ Structured Data │ │ Vector Memory   │
              │                 │ │                 │
              │ conversations   │ │ embeddings      │
              │ preferences     │ │ semantic search │
              │ milestones      │ │                 │
              └─────────────────┘ └─────────────────┘

---

## Technologies Used

- Python
- FastAPI
- SQLite
- SQLAlchemy
- ChromaDB
- Sentence Transformers
- Docker
- Docker Compose
- Pydantic

---

## Project Structure


AI_Academic_Advisor/
│
├── docker-compose.yml
├── .env.example
├── submission.json
├── README.md
│
├── docs/
│ └── memory_architecture.png
│
├── mcp_server/
│ ├── Dockerfile
│ ├── requirements.txt
│ └── app/
│ ├── server.py
│ ├── database.py
│ ├── models.py
│ ├── memory_schemas.py
│ ├── vector_store.py
│ └── tools.py
│
├── agent/
│ ├── Dockerfile
│ ├── requirements.txt
│ └── agent.py
│
└── data/


---

## Memory Schemas

### Conversation

Stores dialogue history between the user and the AI advisor.

Fields:

- user_id
- turn_id
- role
- content
- timestamp

### UserPreferences

Stores user-specific preferences.

Fields:

- user_id
- preferences (JSON dictionary)

### Milestone

Tracks academic achievements or plans.

Fields:

- user_id
- milestone_id
- description
- status
- date_achieved

---

## MCP Memory Tools

The MCP server exposes three primary tools for memory interaction.

### memory_write

Stores new memory entries in the system.

Actions:
- Validates input using Pydantic
- Writes structured data to SQLite
- Generates embeddings for text
- Stores embeddings in ChromaDB

---

### memory_read

Retrieves structured memory from the SQLite database.

Example use cases:
- Retrieve last N conversation turns
- Fetch user preferences
- Access milestone history

---

### memory_retrieve_by_context

Performs semantic search over vector memory.

Steps:
1. Convert query into embedding
2. Search ChromaDB for similar vectors
3. Return relevant past memories

---

## Running the Project

### Prerequisites

- Docker
- Docker Compose

### Start the System


docker compose up --build


This command starts all required services including the MCP server.

---

### Verify Server Health


curl http://localhost:8000/health


Expected response:


{"status":"ok"}


---

### List Available Tools


curl http://localhost:8000/tools


---

## Example Memory Interaction

### Store Conversation


POST /invoke/memory_write


Request:


{
"memory_type": "conversation",
"data": {
"user_id": "test_user_01",
"turn_id": 1,
"role": "user",
"content": "I want to study machine learning"
}
}


---

### Retrieve Conversation History


POST /invoke/memory_read


---

### Semantic Memory Retrieval


POST /invoke/memory_retrieve_by_context


Query example:


"What subjects does the student want to study?"


The system retrieves semantically related memory even if the wording differs.

---

## Example Interaction


User: I want to study AI

Advisor: That's a great field to explore.

User: What did I say earlier?

Advisor: You previously mentioned that you want to study AI.


---

## Submission Files

The repository includes required files for evaluation:

- docker-compose.yml
- .env.example
- README.md
- submission.json
- docs/memory_architecture.png

---

## Future Improvements

- Add real LLM integration (Claude / OpenAI / Ollama)
- Improve agent decision logic for tool usage
- Implement conversation summarization
- Add caching and memory ranking
- Deploy using Kubernetes for scalability

---

## Conclusion

This project demonstrates how AI systems can achieve **persistent, context-aware behavior** by combining structured databases with vector memory retrieval under the MCP architecture.

The result is a modular AI agent capable of maintaining long-term relationships with users while remaining scalable and maintainable