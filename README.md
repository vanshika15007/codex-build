# Nova Chat Studio (React + FastAPI + Gemini-ready)

A polished, more playful chatbot app with:
- a classy chat UI
- general-purpose conversation support
- optional Gemini API integration
- a built-in mini game (Guess the Number)

## Features

- **General chatbot** (not limited to admission/course only)
- **Gemini API support** via backend env vars
- **Fallback local responses** when Gemini key is missing
- **Quick prompt buttons** for fast interactions
- **Mini game mode** (Guess a number from 1-20)

## Project structure

- `src/` – React frontend
- `backend/` – FastAPI backend

## Run locally

### 1) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 2) Frontend

```bash
npm install
npm run dev
```

## Environment variables

### Frontend

```bash
export VITE_API_BASE_URL="http://127.0.0.1:8000"
```

### Backend (optional Gemini)

```bash
export GEMINI_API_KEY="your_api_key_here"
export GEMINI_MODEL="gemini-1.5-flash"
```

If `GEMINI_API_KEY` is not set, backend will use local fallback responses.

## API

### `POST /chat`

```json
{ "text": "Give me a productivity routine" }
```

### `GET /health`

```json
{ "status": "ok" }
```
