from core.logger import get_logger
logger = get_logger("local_rules")

def local_scan(text):
    logger.info("Running local rule-based scan")
    logger.debug(f"Text length: {len(text)}")

    block = ["scam", "phishing", "kill", "idiot", "bitch"]

    if any(w in text.lower() for w in block):
        logger.warning("Local rules blocked content")
        return {"status": "blocked", "clean": False, "message": "🔴 Local rules blocked harmful content."}

    logger.info("Local rules approved content")
    return {"status": "allowed", "clean": True, "message": "🟢 Local rules approved content."}
