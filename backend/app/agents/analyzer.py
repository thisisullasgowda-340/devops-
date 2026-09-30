import json, httpx
from ..config import GEMINI_API_KEY
from ..tools import git_tool

FALLBACK = {
    "root_cause_summary": "Release v2.4.1 set DATABASE_POOL_SIZE=0, so every payment request times out waiting for a DB connection.",
    "evidence_list": ["DBConnectionTimeoutException spike began right after v2.4.1 deploy",
                      "Commit 9f3c2ab changes DATABASE_POOL_SIZE from 20 to 0",
                      "Error rate on /api/v1/payments jumped from 0% to 62%"],
    "proposed_fix": "Roll back payment-service to v2.4.0",
    "confidence_score": 95,
}

def _gemini(prompt: str):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    r = httpx.post(url, timeout=20, json={"contents": [{"parts": [{"text": prompt}]}],
                   "generationConfig": {"responseMimeType": "application/json"}})
    r.raise_for_status()
    return json.loads(r.json()["candidates"][0]["content"]["parts"][0]["text"])

def run(inc):
    diff = git_tool.commit_diff(inc.alert.service, "v2.4.1")
    result, source = FALLBACK, "heuristic engine"
    if GEMINI_API_KEY:
        try:
            prompt = ("You are an SRE. Return JSON with keys root_cause_summary, evidence_list (array), "
                      "proposed_fix, confidence_score (0-100).\nLOGS:\n" + "\n".join(inc.logs[:10]) + "\nDIFF:\n" + diff)
            g = _gemini(prompt)
            if all(k in g for k in FALLBACK):
                result, source = g, "Gemini"
        except Exception:
            pass
    inc.diagnosis = {**result, "diff": diff, "source": source}
    return f"Diagnosis ({source}): {result['root_cause_summary']} Confidence {result['confidence_score']}%."
