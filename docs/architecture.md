# System Architecture

## High-Level Architecture

```mermaid
flowchart TD
    User([Patient / Visitor]) -->|types or speaks| React[React + TypeScript Frontend]
    React -->|Web Speech API| STT[Speech-to-Text]
    React -->|SpeechSynthesis API| TTS[Text-to-Speech]
    React -->|REST / Axios| FastAPI[FastAPI Backend]

    FastAPI --> Auth[JWT Auth]
    FastAPI --> RAG[RAG Pipeline]
    FastAPI --> DB[(SQLite / PostgreSQL)]
    FastAPI --> Analytics[Analytics Events]

    RAG --> Loader[Document Loader]
    Loader --> Chunker[Chunking]
    Chunker --> Embedder[Sentence-Transformers\n / TF-IDF fallback]
    Embedder --> VectorStore[(In-memory Vector Store)]
    VectorStore --> Retriever[Similarity Retriever]
    Retriever --> PromptBuilder[Prompt Builder]
    PromptBuilder --> Gemini[Gemini API]
    Gemini --> FastAPI

    Analytics --> Dashboard[Admin Dashboard\nRecharts]
    DB --> Dashboard
```

## Data Flow (Chat Request)

```mermaid
sequenceDiagram
    participant U as User
    participant F as React Frontend
    participant A as FastAPI /api/chat
    participant R as RAG Retriever
    participant G as Gemini API
    participant D as Database

    U->>F: Types or speaks a question
    F->>A: POST /api/chat {message, language}
    A->>A: Emergency keyword check
    A->>R: retrieve(message)
    R-->>A: top-k knowledge chunks
    A->>G: prompt(system + context + question)
    G-->>A: generated answer
    A->>D: log ChatHistory + AnalyticsEvent
    A-->>F: {reply, department_matched, sources}
    F->>U: Displays + speaks reply
```

## Deployment Architecture

```mermaid
flowchart LR
    subgraph Vercel
        FE[React Frontend - Vite build]
    end
    subgraph Render/Docker
        BE[FastAPI Backend]
        DB[(SQLite volume\nor managed Postgres)]
    end
    FE -->|HTTPS REST| BE
    BE --> DB
    BE -->|API calls| Gemini[Gemini API]
```

## Why SQLite + in-memory vectors instead of Postgres + ChromaDB
For a hackathon-scale build, SQLite (via SQLAlchemy) and an in-memory
NumPy vector store remove all external infrastructure dependencies —
the whole stack runs with `uvicorn app.main:app` and `npm run dev`,
no database server or vector DB container required. Both are drop-in
replaceable: swap `DATABASE_URL` to a Postgres DSN, or swap
`app/rag/vector_store.py` for a ChromaDB-backed implementation,
without touching any other module — every other layer only calls
`.add()` / `.search()` or standard SQLAlchemy sessions.
