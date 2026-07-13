# Tests

Unit and integration tests live alongside their respective apps:

- `backend/tests/` — pytest suite (auth, chat/RAG, departments, doctors,
  feedback, analytics, health checks) run against an in-memory-backed
  SQLite test database via FastAPI's `TestClient`.
- `frontend/tests/` — Vitest + React Testing Library (component
  rendering, i18n key parity, interaction tests).

This top-level `tests/` directory is reserved for end-to-end tests that
span both apps (e.g. Playwright/Cypress flows) as the project grows.
