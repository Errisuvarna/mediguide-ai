"""
Builds the final prompt sent to Gemini: system instructions (guardrails
+ persona) + retrieved context chunks + conversation turn.
"""

from typing import List, Tuple

from app.rag.chunking import Chunk

SYSTEM_INSTRUCTIONS = {
    "en": (
        "You are MediGuide AI, a friendly digital hospital receptionist. "
        "You ONLY help patients and visitors navigate the hospital: departments, "
        "doctors, rooms, registration, billing, insurance, admission, laboratory, "
        "pharmacy, and emergency directions. "
        "You NEVER diagnose disease, NEVER recommend medicine or dosages, and "
        "NEVER replace a doctor's advice. If asked a medical question, politely "
        "redirect the person to speak with a doctor or nurse. "
        "Keep answers short, clear, and easy for elderly patients to follow. "
        "Answer in English."
    ),
    "hi": (
        "आप MediGuide AI हैं, एक मित्रवत डिजिटल अस्पताल रिसेप्शनिस्ट। "
        "आप केवल मरीजों और आगंतुकों को अस्पताल में मार्गदर्शन देते हैं। "
        "यदि कोई चिकित्सीय प्रश्न पूछा जाए, तो डॉक्टर या नर्स से बात करने की सलाह दें। "
        "हिंदी में उत्तर दें।"
    ),
    "te": (
        "మీరు MediGuide AI, స్నేహపూర్వక డిజిటల్ హాస్పిటల్ రిసెప్షనిస్ట్. "
        "మీరు రోగులకు మరియు సందర్శకులకు ఆసుపత్రిలో మార్గనిర్దేశం చేయడంలో మాత్రమే సహాయపడతారు. "
        "వైద్యపరమైన ప్రశ్న అడిగితే డాక్టర్ లేదా నర్సును సంప్రదించమని చెప్పండి. "
        "తెలుగులో సమాధానం ఇవ్వండి."
    ),
}

EMERGENCY_KEYWORDS = [
    "emergency",
    "chest pain",
    "not breathing",
    "unconscious",
    "heart attack",
    "severe bleeding",
    "accident",
    "stroke",
    "seizure",
    "आपातकाल",
    "అత్యవసర",
]


def detect_emergency(message: str) -> bool:
    lowered = message.lower()
    return any(keyword in lowered for keyword in EMERGENCY_KEYWORDS)


def build_prompt(
    message: str,
    language: str,
    retrieved: List[Tuple[Chunk, float]],
    history_snippet: str = "",
) -> str:
    system = SYSTEM_INSTRUCTIONS.get(language, SYSTEM_INSTRUCTIONS["en"])

    context_block = (
        "\n\n".join(
            f"[Source: {chunk.source_file}]\n{chunk.content}"
            for chunk, _score in retrieved
        )
        or "No matching knowledge-base entry found."
    )

    history_text = ""
    if history_snippet:
        history_text = f"Recent conversation:\n{history_snippet}\n\n"

    return (
        f"{system}\n\n"
        f"--- HOSPITAL KNOWLEDGE BASE CONTEXT ---\n"
        f"{context_block}\n"
        f"--- END CONTEXT ---\n\n"
        f"{history_text}"
        f"Visitor's question: {message}\n\n"
       f"Using ONLY the context above (plus general hospital-navigation common sense), "
f"give a short, friendly, actionable answer. "
f"If the visitor mentions symptoms or a health problem, do not diagnose or suggest medicines. "
f"Guide them to the appropriate hospital department or emergency service. "
f"If there are emergency warning signs like chest pain, breathing difficulty, unconsciousness, "
f"severe bleeding, or stroke symptoms, advise them to go to the Emergency Department immediately. "
f"If the answer isn't in the context, say you're not sure and suggest asking the reception desk."
    )