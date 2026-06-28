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
    "I can help with study plans, programming concepts, career preparation, and real-world project ideas. Tell me the topic and your goal.",
    "Ask for a practical roadmap, project plan, interview prep, or concept explanation — I can give you structured guidance for each.",
    "Need a clear learning path, sample project, or mock interview question? I can provide that without requiring extra details.",
]

greeting_patterns = [
    re.compile(r"^(hi|hello|hey|good morning|good afternoon|good evening)\b"),
]

math_application_patterns = [
    re.compile(r"\breal[- ]world math applications?\b"),
    re.compile(r"\bmath applications?\b"),
]

roadmap_patterns = [
    re.compile(r"\broadmap\b"),
    re.compile(r"\bdata science\b"),
    re.compile(r"\bmachine learning\b"),
    re.compile(r"\bcareer path\b"),
]

topic_response_patterns = [
    (
        re.compile(r"\bpython\b"),
        (
            "Python is a versatile language used for web development, data science, automation, and scripting.\n"
            "I can help you with a learning plan, sample projects, or interview prep for Python."
        ),
    ),
    (
        re.compile(r"\bmachine learning\b"),
        (
            "Machine learning is used to build models that learn from data and make predictions.\n"
            "Start with supervised learning, then practice with real datasets and simple projects."
        ),
    ),
    (
        re.compile(r"\bmachine\b"),
        (
            "Machine learning is a practical field for predictive modeling, data science, and real-world applications.\n"
            "Ask me for a roadmap, project idea, or study plan to learn it step by step."
        ),
    ),
    (
        re.compile(r"\bdata science\b"),
        (
            "Data science combines statistics, programming, and domain knowledge to analyze data and solve problems.\n"
            "I can give you a study plan, project idea, or interview prep specific to data science."
        ),
    ),
    (
        re.compile(r"\bprogramming\b"),
        (
            "Programming is about solving problems with code.\n"
            "Tell me the language or project area you want to learn, and I will give you a clear path."
        ),
    ),
    (
        re.compile(r"\bsql\b"),
        (
            "SQL is the language for querying databases and analyzing structured data.\n"
            "I can explain queries, design exercises, or create a learning plan for SQL."
        ),
    ),
    (
        re.compile(r"\bweb development\b"),
        (
            "Web development includes front-end and back-end skills for building websites and web apps.\n"
            "I can suggest project ideas, learning resources, or interview preparation for web development."
        ),
    ),
    (
        re.compile(r"\bcareer\b"),
        (
            "A strong career path starts with focused skills, projects, and interview readiness.\n"
            "I can help you build a professional roadmap, portfolio strategy, or mock interview routine."
        ),
    ),
    (
        re.compile(r"\bproject\b"),
        (
            "A useful project should combine learning, real outcomes, and clear steps.\n"
            "I can recommend a professional project plan in areas like data science, web apps, or automation."
        ),
    ),
    (
        re.compile(r"\bfull stack\b"),
        (
            "Full stack development covers both front-end and back-end technologies in a single project.\n"
            "A typical path includes: HTML/CSS/JavaScript → React or Vue → Node.js or Python → Databases → Deployment. I can build a structured learning plan or suggest a portfolio project."
        ),
    ),
    (
        re.compile(r"\bai\b"),
        (
            "Artificial Intelligence spans machine learning, deep learning, NLP, and generative models.\n"
            "Start with Python fundamentals, then move to ML basics, advanced neural networks, and practical AI projects. I can create a step-by-step roadmap or suggest real-world AI project ideas."
        ),
    ),
    (
        re.compile(r"\bartificial intelligence\b"),
        (
            "Artificial Intelligence spans machine learning, deep learning, NLP, and generative models.\n"
            "Start with Python fundamentals, then move to ML basics, advanced neural networks, and practical AI projects. I can create a step-by-step roadmap or suggest real-world AI project ideas."
        ),
    ),
    (
        re.compile(r"\bclimate change\b"),
        (
            "Here are actionable climate change solutions:\n"
            "1. Renewable Energy: Shift to solar, wind, and hydroelectric power.\n"
            "2. Energy Efficiency: Improve building insulation and use efficient appliances.\n"
            "3. Carbon Capture: Deploy technology to remove CO2 from the atmosphere.\n"
            "4. Reforestation: Restore forests to absorb carbon and protect ecosystems.\n"
            "5. Sustainable Transport: Switch to EVs and improve public transit.\n"
            "6. Circular Economy: Reduce waste through recycling and sustainable production.\n"
            "7. Agriculture Reform: Shift to regenerative farming and reduce methane emissions.\n"
            "Individual actions: reduce consumption, choose renewable energy, advocate for policy change."
        ),
    ),
]

games_patterns = [
    re.compile(r"\bgames?\b"),
    re.compile(r"\bgame development\b"),
    re.compile(r"\bgame design\b"),
]

interview_patterns = [
    re.compile(r"\binterview\b"),
    re.compile(r"\bcase study\b"),
    re.compile(r"\bscenario\b"),
    re.compile(r"\bmock interview\b"),
]

study_plan_patterns = [
    re.compile(r"\bstudy plan\b"),
    re.compile(r"\bprepare\b"),
    re.compile(r"\bexam prep\b"),
    re.compile(r"\bplan for\b"),
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

    if matches_any(normalized_text, roadmap_patterns):
        return (
            "A practical data science roadmap looks like this:\n"
            "1. Learn Python, data analysis, and statistics fundamentals.\n"
            "2. Practice with datasets using pandas, NumPy, and visualization tools.\n"
            "3. Study machine learning basics: regression, classification, and model evaluation.\n"
            "4. Build real projects: data cleaning, dashboards, prediction models, and storytelling.\n"
            "5. Share your work in a portfolio, and review interview-style case questions."
        )

    for pattern, response in topic_response_patterns:
        if pattern.search(normalized_text):
            return response

    if matches_any(normalized_text, games_patterns):
        return (
            "If you want to explore games, I can help with game dev learning paths, "
            "project ideas, or how game design connects to problem solving.\n"
            "You can ask for a game development roadmap, sample project, or study plan for game-focused skills."
        )

    if matches_any(normalized_text, interview_patterns):
        return (
            "For interview prep, I can create sample questions, answer strategies, or case-study walkthroughs.\n"
            "Tell me the subject or role you want to prepare for, and I will give you a structured plan."
        )

    if matches_any(normalized_text, study_plan_patterns):
        return (
            "Here is a helpful study plan structure:\n"
            "1. Define your goal and timeline.\n"
            "2. Break topics into daily or weekly modules.\n"
            "3. Alternate learning, practice, and review sessions.\n"
            "4. Use small projects or sample problems to apply concepts.\n"
            "5. Track progress and adjust based on what feels hard or easy."
        )

    for topic, patterns in compiled_aliases.items():
        if matches_any(normalized_text, patterns):
            return knowledge_base[topic]

    return None


def fallback_response() -> str:
    return random.choice(generic_fallbacks)
