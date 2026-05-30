import os
import boto3
from core.logger import get_logger

logger = get_logger("aws_guardrails")

def aws_moderate(text):
    if not os.getenv("AWS_GUARDRAIL_ID"):
        logger.info("AWS Guardrails disabled")
        return {"status": "allowed", "clean": True, "message": "🟢 AWS skipped."}

    logger.info("Sending content to AWS Bedrock Guardrails")
    logger.debug(f"Payload length: {len(text)}")

    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    try:
        response = client.apply_guardrail(
            guardrailIdentifier=os.getenv("AWS_GUARDRAIL_ID"),
            guardrailVersion="DRAFT",
            source="INPUT",
            content=[{"text": {"text": text}}]
        )

        if response.get("action") == "GUARDRAIL_INTERVENED":
            logger.warning("AWS blocked content")
            return {"status": "blocked", "clean": False, "message": "🔴 AWS blocked harmful content."}

        logger.info("AWS approved content")
        return {"status": "allowed", "clean": True, "message": "🟢 AWS approved content."}

    except Exception as e:
        logger.error(f"AWS error: {e}")
        return {"status": "allowed", "clean": True, "message": "🟢 AWS fallback."}
