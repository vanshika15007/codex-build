import random
import re

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

compiled_aliases = {
    topic: [re.compile(rf"\b{re.escape(keyword.lower())}\b") for keyword in keywords]
    for topic, keywords in aliases.items()
}

generic_fallbacks = [
    "I can help with study plans, concept explanations, and professional real-world problem solving. Ask for a step-by-step plan.",
    "Try asking for a project roadmap, exam preparation schedule, or interview-style case analysis.",
    "I support educational and professional growth topics, including productivity, learning strategy, and practical applications.",
]

greeting_patterns = [
    re.compile(r"^(hi|hello|hey|good morning|good afternoon|good evening)\b"),
]

math_application_patterns = [
    re.compile(r"\breal[- ]world math applications?\b"),
    re.compile(r"\bmath applications?\b"),
]

help_patterns = [
    re.compile(r"^how\??$"),
    re.compile(r"^help\??$"),
    re.compile(r"^what can you do\??$"),
    re.compile(r"^how can you help\??$"),
]


def matches_any(text: str, patterns: list[re.Pattern[str]]) -> bool:
    return any(pattern.search(text) for pattern in patterns)


def build_rule_based_response(text: str) -> str | None:
    normalized_text = text.lower().strip()

    if matches_any(normalized_text, greeting_patterns):
        return (
            "Hi! I can help with study plans, concept explanations, interview-style scenarios, "
            "and practical real-world examples. Try asking for a plan, an explanation, or a list of applications."
        )

    if matches_any(normalized_text, help_patterns):
        return (
            "I can help in a few practical ways: \n"
            "1. Build study plans by subject or deadline.\n"
            "2. Explain concepts in simple steps.\n"
            "3. Give real-world applications and project ideas.\n"
            "4. Practice interview-style or scenario-based questions.\n"
            "Tell me your topic and goal, and I will tailor the answer."
        )

    if matches_any(normalized_text, math_application_patterns):
        return (
            "Here are 5 real-world math applications:\n"
            "1. Budgeting and personal finance for tracking savings, loans, and interest.\n"
            "2. Construction and architecture for measurements, area, volume, and structural planning.\n"
            "3. Data analysis in business for forecasting sales and spotting trends.\n"
            "4. Computer graphics and game development for geometry, vectors, and motion.\n"
            "5. Medicine and public health for dosage calculations, statistics, and risk analysis."
        )

    for topic, patterns in compiled_aliases.items():
        if matches_any(normalized_text, patterns):
            return knowledge_base[topic]

    return None


def fallback_response() -> str:
    return random.choice(generic_fallbacks)
