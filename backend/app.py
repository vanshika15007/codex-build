from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

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
    "admission": "Admissions are open from June to August. Apply through the official college portal.",
    "fees": "The annual fee ranges between ₹50,000 and ₹1,20,000 depending on the course.",
    "exam": "Exams are conducted semester-wise with internal and final assessments.",
    "course": "We offer B.Tech, BCA, BBA, MBA, MCA and various professional programs.",
    "placement": "Our placement rate is 92% with top companies visiting campus every year.",
    "hostel": "Separate hostel facilities are available for boys and girls with full security.",
    "library": "Our library has over 50,000 books and digital learning resources.",
}

greetings = [
    "Hello 👋 How can I assist you today?",
    "Hi there! 🎓 Ask me anything about the college.",
    "Welcome! 😊 I'm your AI Student Assistant.",
]

fallback_responses = [
    "That’s an interesting question! Our AI system is continuously improving.",
    "I understand your query. Please contact the admin office for detailed information.",
    "Great question! Let me guide you with available information.",
]


@app.post("/chat")
async def chat(message: Message):
    text = message.text.lower()

    # Greeting detection
    if any(word in text for word in ["hi", "hello", "hey"]):
        return {"response": random.choice(greetings)}

    # Knowledge base search
    for keyword in knowledge_base:
        if keyword in text:
            return {"response": knowledge_base[keyword]}

    # Default fallback
    return {"response": random.choice(fallback_responses)}
