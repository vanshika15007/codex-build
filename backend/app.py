import json
import os
import random
from urllib import error, parse, request

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
app = FastAPI(title="Nova Chatbot API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    text: str


# Smart knowledge base
knowledge_base = {
    "admission": "Admissions are open from June to August. You can apply through the official portal.",
    "fees": "The annual fee ranges between ₹50,000 and ₹1,20,000 based on course and scholarships.",
    "exam": "Exams are semester-wise with internal + final assessments.",
    "course": "Popular programs include B.Tech, BCA, BBA, MBA, and MCA.",
    "placement": "Placement support includes resume workshops, mock interviews, and aptitude prep.",
    "hostel": "Separate hostels with security, Wi-Fi, and mess are available.",
    "library": "Library access includes physical books, journals, and digital resources.",
}

aliases = {
    "admission": ["admission", "apply", "application", "enroll", "enrolment"],
    "fees": ["fees", "fee", "cost", "tuition", "scholarship"],
    "exam": ["exam", "examination", "test", "semester"],
    "course": ["course", "courses", "program", "degree", "branch"],
    "placement": ["placement", "placements", "job", "recruitment", "career"],
    "hostel": ["hostel", "accommodation", "room", "mess"],
    "library": ["library", "books", "journal", "digital resources"],
}

greetings = ["hi", "hello", "hey", "good morning", "good evening"]

generic_fallbacks = [
    "I can answer general questions, help with ideas, and also assist with student topics. Try asking me anything!",
    "I’m ready for both casual and academic chats. You can ask for explanations, plans, or creative ideas.",
    "Want to play? Try the Guess Game button in the UI, or ask me for a quiz question.",
]
def ask_gemini(prompt: str) -> str | None:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key="
        f"{parse.quote(api_key)}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "You are Nova, a friendly and concise chatbot. Help users with general, educational, and creative queries. "
                        f"User message: {prompt}"
                    }
                ]
            }
        ]
    }

    req = request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=12) as res:
            body = json.loads(res.read().decode("utf-8"))
            candidates = body.get("candidates", [])
            if not candidates:
                return None
            parts = candidates[0].get("content", {}).get("parts", [])
            if not parts:
                return None
            return parts[0].get("text")
    except (error.URLError, TimeoutError, json.JSONDecodeError, KeyError):
        return None


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat")
async def chat(message: Message):
    text = message.text.lower().strip()

    if not text:
        return {"response": "Please type a message so I can help."}

    # Greeting detection
    gemini_response = ask_gemini(message.text.strip())
    if gemini_response:
        return {"response": gemini_response}

    # Knowledge base search
    for topic, keywords in aliases.items():
        if any(keyword in text for keyword in keywords):
            return {"response": knowledge_base[topic]}

    # Default fallback
    return {"response": random.choice(generic_fallbacks)}
