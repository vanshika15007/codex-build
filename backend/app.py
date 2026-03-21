import json
import os
import random
from urllib import error, parse, request

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="Nova Chatbot API", version="2.1.0")

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
    "career": "For career growth, focus on practical projects, internships, communication skills, and a strong portfolio.",
    "real_world": "Try solving real-world problems by defining the issue, collecting data, testing small solutions, and measuring impact.",
}

aliases = {
    "admission": ["admission", "apply", "application", "enroll", "enrolment"],
    "fees": ["fees", "fee", "cost", "tuition", "scholarship"],
    "exam": ["exam", "examination", "test", "semester"],
    "course": ["course", "courses", "program", "degree", "branch"],
    "placement": ["placement", "placements", "job", "recruitment", "career fair"],
    "hostel": ["hostel", "accommodation", "room", "mess"],
    "library": ["library", "books", "journal", "digital resources"],
    "career": ["career", "resume", "interview", "internship", "portfolio"],
    "real_world": ["real world", "case study", "problem solving", "project", "impact"],
}

generic_fallbacks = [
    "I can help with study plans, concept explanations, and professional real-world problem solving. Ask for a step-by-step plan.",
    "Try asking for a project roadmap, exam preparation schedule, or interview-style case analysis.",
    "I support educational and professional growth topics, including productivity, learning strategy, and practical applications.",
]
def ask_gemini(prompt: str) -> str | None:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment")
        return None

    model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    url = (
        f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key="
        f"{parse.quote(api_key)}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "You are Nova, a professional learning assistant. Be concise, structured, and practical. "
                        "Provide actionable, real-world study advice when relevant. "
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
                print("❌ No candidates in Gemini response")
                return None
            parts = candidates[0].get("content", {}).get("parts", [])
            if not parts:
                print("❌ No parts in Gemini response")
                return None
            response_text = parts[0].get("text")
            print(f"✅ Gemini API success")
            return response_text
    except error.URLError as e:
        print(f"❌ Gemini URLError: {e}")
        return None
    except TimeoutError as e:
        print(f"❌ Gemini Timeout: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Gemini JSON decode error: {e}")
        return None
    except Exception as e:
        print(f"❌ Gemini unexpected error: {e}")
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
