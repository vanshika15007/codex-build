# Nova Professional Study Copilot (React + FastAPI + Gemini-ready)

A more professional chatbot experience designed for students and early professionals.

## What’s improved

- **Professional chat interface** with cleaner structure and focused study workflow
- **Scenario-based game** for real-world decision making (A/B/C challenge)
- **Curated video resources** for high-quality learning (Khan Academy, MIT OCW, CrashCourse, TED-Ed)
- **Gemini API support** through backend environment variables
- **Smart fallback responses** for educational and career-oriented questions

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
{ "text": "Build a practical study plan for the next 7 days" }
```

### `GET /health`

```json
{ "status": "ok" }
```
