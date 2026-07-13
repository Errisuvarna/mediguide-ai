# Build context is the project ROOT (see docker-compose.yml), because this
# image needs both backend/ and the top-level dataset/ + knowledge_base/
# directories that the seed script and RAG pipeline read at startup.
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ /app/
COPY dataset/ /app/dataset/
COPY knowledge_base/ /app/knowledge_base/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
