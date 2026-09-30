import httpx
from ..config import SLACK_WEBHOOK_URL
def classify(inc):
    inc.action = {"type": "rollback", "target": "v2.4.0", "risk": "HIGH_RISK",
                  "label": "Approve Rollback to v2.4.0"}
    if SLACK_WEBHOOK_URL:
        try:
            httpx.post(SLACK_WEBHOOK_URL, timeout=5, json={"text": f"[{inc.id}] Approval needed: rollback {inc.alert.service} to v2.4.0"})
        except Exception:
            pass
    return "Rollback to v2.4.0 classified HIGH_RISK. Awaiting human approval."
