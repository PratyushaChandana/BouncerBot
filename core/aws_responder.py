import os
import json
import boto3
from botocore.exceptions import ClientError
from core.logger import get_logger

logger = get_logger("aws_responder")

def generate_ai_response(user_text):
    logger.info("Generating AI response using AWS Bedrock")

    try:
        # Create Bedrock Runtime client
        client = boto3.client(
            "bedrock-runtime",
            region_name=os.getenv("AWS_REGION", "us-west-2")
        )

        # Request body (Bedrock Messages API)
        body = {
            "messages": [
                {"role": "system", "content": "You are Bouncer bot AI. Respond concisely, safely, and helpfully."},
                {"role": "user", "content": user_text}
            ],
            "max_tokens": 200,
            "temperature": 0.7
        }

        # Use a cheap ON-DEMAND model (works instantly)
        response = client.invoke_model(
            modelId="qwen.qwen3-32b-v1:0",
            body=json.dumps(body)
        )

        # Read raw response
        result = response["body"].read().decode("utf-8")
        parsed = json.loads(result)

        # -------------------------------
        # UNIVERSAL RESPONSE PARSER
        # -------------------------------
        reply = None

        # 1. Anthropic-style (content[0].text)
        if "content" in parsed and isinstance(parsed["content"], list):
            item = parsed["content"][0]
            if isinstance(item, dict) and "text" in item:
                reply = item["text"]

        # 2. Qwen / DeepSeek / Mistral (output_text)
        if reply is None and "output_text" in parsed:
            reply = parsed["output_text"]

        # 3. Message-style (message.content)
        if reply is None and "message" in parsed:
            msg = parsed["message"]
            if isinstance(msg, dict) and "content" in msg:
                reply = msg["content"]

        # 4. OpenAI-style (choices[0].message.content)
        if reply is None and "choices" in parsed:
            try:
                reply = parsed["choices"][0]["message"]["content"]
            except Exception:
                pass

        # 5. Llama-style (generation)
        if reply is None and "generation" in parsed:
            reply = parsed["generation"]

        # 6. Fallback: return entire JSON
        if reply is None:
            reply = str(parsed)

        return reply

    except ClientError as e:
        # AWS-specific error details
        logger.error("AWS ClientError occurred")
        logger.error(f"Error code: {e.response['Error'].get('Code')}")
        logger.error(f"Error message: {e.response['Error'].get('Message')}")
        logger.error(f"HTTP status: {e.response.get('ResponseMetadata', {}).get('HTTPStatusCode')}")
        logger.error(f"Request ID: {e.response.get('ResponseMetadata', {}).get('RequestId')}")
        logger.error(f"Full error: {e}")

        return "⚠️ AWS authentication or model error. Check logs for details."

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return "⚠️ Unexpected AWS error. Check logs for details."
