from flask import Flask, request, jsonify, render_template
from core.verdict_engine import evaluate_content
from core.strike_manager import StrikeManager
from core.aws_responder import generate_ai_response
from core.logger import get_logger

logger = get_logger("app")

app = Flask(__name__)
strikes = StrikeManager()

@app.route("/")
def home():
    logger.info("Rendering UI")
    return render_template("index.html")

@app.route("/message", methods=["POST"])
def message_handler():
    data = request.get_json() or {}
    user_text = data.get("message", "")
    session_id = data.get("session_id")  # <-- browser localStorage ID
    user_id = request.remote_addr

    logger.info(f"Incoming message from {user_id}")
    logger.debug(f"Payload: {data}")

    # Intro handshake
    if user_text == "__init__":
        logger.info("Sending Bouncer bot intro")
        return jsonify({"reply": "🛡️ Bouncer bot online. State your query?"})

    # Ban check
    if strikes.is_banned(user_id):
        logger.warning(f"Banned user attempted access: {user_id}")
        return jsonify({"reply": "⛔ Access denied. You are banned due to repeated violations."})

    # Evaluate content
    verdict = evaluate_content(user_text)
    verdict_status = verdict.get("status")
    logger.info(f"Verdict returned: {verdict}")

    # Blocked content → strike + warning
    if verdict_status == "blocked":
        warning = strikes.add_strike(user_id)
        logger.warning(f"Strike issued to {user_id}: {warning}")
        return jsonify({"reply": warning})

    # Clean content → upload + AI response
    if verdict.get("clean"):
        # Generate AI reply FIRST
        ai_reply = generate_ai_response(user_text)

        # Upload structured log
        try:
            from core.box_client import upload_structured_log
            upload_structured_log(session_id, user_text, ai_reply, verdict_status)
        except Exception as e:
            logger.error(f"Box upload failed: {e}")

        return jsonify({"reply": ai_reply})

    # Fallback for unexpected verdicts
    return jsonify({"reply": verdict.get("message", "⚠️ Unable to process message.")})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
