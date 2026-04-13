#!/bin/sh
set -e

if [ ! -f /app/storage/index.faiss ]; then
  python3 -m app.indexar
fi

exec uvicorn api.api:app --host 0.0.0.0 --port 8000