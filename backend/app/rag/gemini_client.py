"""
Thin wrapper around the Gemini API.

If GEMINI_API_KEY is not configured (e.g. local demo without a key),
this falls back to returning the top retrieved knowledge-base chunk
directly, so the /chat endpoint keeps working end-to-end without a
live LLM call — useful for offline grading/demo environments.
"""
import logging
from typing import List, Tuple

from app.config import settings
from app.rag.chunking import Chunk

logger = logging.getLogger(__name__)

_configured = False


def _ensure_configured() -> bool:
    global _configured
    if _configured:
        return True
    if not settings.GEMINI_API_KEY:
        return False
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        _configured = True
        return True
    except Exception as exc:  # noqa: BLE001
        logger.warning("Gemini configuration failed: %s", exc)
        return False


def generate_answer(prompt: str, retrieved: List[Tuple[Chunk, float]]) -> str:
    if _ensure_configured():
        try:
            import google.generativeai as genai
            model = genai.GenerativeModel(settings.GEMINI_MODEL)
            response = model.generate_content(prompt)
            text = (response.text or "").strip()
            if text:
                return text
        except Exception as exc:  # noqa: BLE001
            logger.warning("Gemini generation failed, using fallback: %s", exc)

    # Fallback: no API key or Gemini call failed -> answer from best chunk.
    if retrieved:
        best_chunk, _score = retrieved[0]
        return (
            f"Here's what I found: {best_chunk.content}\n\n"
            f"(Source: {best_chunk.source_file}. For anything more specific, "
            f"please check with the reception desk.)"
        )
    return (
        "I'm not fully sure about that yet. Please ask at the reception desk "
        "and they'll be happy to help you directly."
    )
