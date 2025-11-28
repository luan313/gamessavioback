#!/usr/bin/env bash

echo "🔍 Detectando sistema operacional..."

OS="$(uname -s)"

echo "➡ Sistema detectado: $OS"

echo "📦 Instalando dependências do requirements.txt..."

if [[ "$OS" == "Linux" || "$OS" == "Darwin" ]]; then
    python3 -m pip install -r requirements.txt
else
    python -m pip install -r requirements.txt
fi

echo "🚀 Iniciando FastAPI com Uvicorn..."

if [[ "$OS" == "Linux" || "$OS" == "Darwin" ]]; then
    python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
else
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
fi
