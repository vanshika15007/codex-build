import json
import os
from urllib import error, parse, request

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from chat_logic import build_rule_based_response, fallback_response

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
            print("✅ Gemini API success")
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

    rule_based_response = build_rule_based_response(text)
    if rule_based_response:
        return {"response": rule_based_response}

    # Greeting detection
    gemini_response = ask_gemini(message.text.strip())
    if gemini_response:
        return {"response": gemini_response}

    # Knowledge base search
    return {"response": fallback_response()}
