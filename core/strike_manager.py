from core.logger import get_logger
logger = get_logger("strike_manager")

class StrikeManager:
    def __init__(self):
        self.violations = {}
        self.limit = 3

    def add_strike(self, user_id):
        self.violations[user_id] = self.violations.get(user_id, 0) + 1
        strikes = self.violations[user_id]

        logger.warning(f"Strike added for {user_id}. Total: {strikes}")

        if strikes == 1:
            return "⚠️ Warning 1: Harmful content detected."
        if strikes == 2:
            return "⚠️ Warning 2: Continued harmful content."
        if strikes >= self.limit:
            return "⛔ You are banned due to repeated violations."

    def is_banned(self, user_id):
        banned = self.violations.get(user_id, 0) >= self.limit
        if banned:
            logger.warning(f"User {user_id} is banned")
        return banned
