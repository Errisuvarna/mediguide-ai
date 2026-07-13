# Folder Structure

```
mediguide-ai/
├── frontend/                  # React + TypeScript + Vite + Tailwind
│   ├── src/
│   │   ├── api/                # Axios client
│   │   ├── components/
│   │   │   ├── Layout/         # Navbar, Footer, Layout
│   │   │   ├── common/         # Button, Card, StatCard, LoadingSpinner
│   │   │   ├── chat/           # ChatBubble, VoiceButton
│   │   │   ├── dashboard/      # Bar/Line/Pie charts, RecentQueriesTable
│   │   │   └── map/            # HospitalMapSvg
│   │   ├── context/            # AuthContext, ThemeContext
│   │   ├── hooks/               # useSpeechRecognition, useSpeechSynthesis
│   │   ├── i18n/                # en/hi/te translations + provider
│   │   ├── pages/               # One file per route (12 pages)
│   │   ├── types/                # Shared TypeScript interfaces
│   │   └── styles/               # Tailwind entry css
│   └── tests/                    # Vitest + Testing Library
│
├── backend/                    # FastAPI + SQLAlchemy
│   ├── app/
│   │   ├── models/               # 16 SQLAlchemy ORM models
│   │   ├── schemas/              # Pydantic request/response schemas
│   │   ├── routers/              # auth, chat, departments, doctors, ...
│   │   ├── core/                 # JWT security
│   │   ├── rag/                  # document_loader, chunking, embeddings,
│   │   │                         # vector_store, retriever, prompt_builder,
│   │   │                         # gemini_client
│   │   ├── seed/                 # seed_db.py loads dataset/ into the DB
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py               # FastAPI app + startup hooks
│   └── tests/                    # pytest suite
│
├── dataset/                    # generate_dataset.py + CSV/JSON/SQL (648 rows)
├── knowledge_base/             # Markdown docs loaded by the RAG pipeline
├── database/                   # schema.sql (reference copy) + ER diagram
├── docs/                       # architecture, folder structure (this file)
├── docker-compose.yml
├── .env.example
└── README.md
```
