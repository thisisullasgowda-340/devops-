import os
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
STEP_DELAY = float(os.getenv("STEP_DELAY", "1.5"))
