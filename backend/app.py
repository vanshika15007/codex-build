import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from groq import Groq

try:
    from backend.chat_logic import build_rule_based_response, fallback_response
except ImportError:
    from chat_logic import build_rule_based_response, fallback_response

# Load environment variables from the backend folder explicitly
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

app = FastAPI(title="Nova Chatbot API", version="2.2.0")

# CORS (allow frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request schema
class Message(BaseModel):
    text: str


# 🔥 Groq API function
def ask_groq(prompt: str) -> str | None:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print("❌ GROQ_API_KEY not found in environment")
        return None

    try:
        client = Groq(api_key=api_key)

        completion = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama3-8b-8192"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Nova, a professional learning assistant. "
                        "Be concise, structured, and practical. "
                        "Provide actionable, real-world study advice when relevant."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.7,
            max_tokens=500,
        )

        response_text = completion.choices[0].message.content
        print("✅ Groq API success")
        return response_text

    except Exception as e:
        print(f"❌ Groq API error: {e}")
        return None


# Health check route
@app.get("/health")
async def health():
    return {"status": "ok"}


# Main chatbot route
@app.post("/chat")
async def chat(message: Message):
    text = message.text.lower().strip()

    # Empty input check
    if not text:
        return {"response": "Please type a message so I can help."}

    # Rule-based responses (fast)
    rule_based_response = build_rule_based_response(text)
    if rule_based_response:
        return {"response": rule_based_response}

    # 🔥 Groq AI response
    groq_response = ask_groq(message.text.strip())
    if groq_response:
        return {"response": groq_response}

    # Fallback response
    return {"response": fallback_response()}
