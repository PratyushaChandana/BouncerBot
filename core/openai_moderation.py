import os
from openai import OpenAI
from core.logger import get_logger

logger = get_logger("openai_moderation")

def openai_moderate(text):
    if not os.getenv("OPENAI_API_KEY"):
        logger.info("OpenAI moderation disabled")
        return {"status": "allowed", "clean": True, "message": "🟢 OpenAI skipped."}

    logger.info("Sending content to OpenAI Moderation API")
    logger.debug(f"Payload length: {len(text)}")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    try:
        res = client.moderations.create(model="omni-moderation-latest", input=text)
        flagged = res.results[0].flagged

        if flagged:
            logger.warning("OpenAI flagged harmful content")
            return {"status": "blocked", "clean": False, "message": "🔴 OpenAI flagged harmful content."}

        logger.info("OpenAI approved content")
        return {"status": "allowed", "clean": True, "message": "🟢 OpenAI approved content."}

    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        return {"status": "allowed", "clean": True, "message": "🟢 OpenAI fallback."}
