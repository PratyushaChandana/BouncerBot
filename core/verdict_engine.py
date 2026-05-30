from core.apify_pipeline import extract_url_content
from core.aws_guardrails import aws_moderate
from core.openai_moderation import openai_moderate
from core.local_rules import local_scan
from core.logger import get_logger

logger = get_logger("verdict_engine")

def evaluate_content(user_text):
    logger.info("Evaluating content through moderation pipeline")
    logger.debug(f"User text: {user_text}")

    scraped = extract_url_content(user_text)
    logger.debug(f"Scraped content length: {len(scraped)}")

    combined = f"User: {user_text}\nScraped: {scraped}"

    logger.info("Running AWS moderation")
    aws_result = aws_moderate(combined)
    logger.debug(f"AWS result: {aws_result}")

    if aws_result["status"] == "blocked":
        logger.warning("AWS blocked content")
        return aws_result

    # logger.info("Running OpenAI moderation")
    # oai_result = openai_moderate(combined)
    # logger.debug(f"OpenAI result: {oai_result}")

    # if oai_result["status"] == "blocked":
    #     logger.warning("OpenAI blocked content")
    #     return oai_result

    logger.info("Running local fallback rules")
    local_result = local_scan(combined)
    logger.debug(f"Local result: {local_result}")

    return local_result
