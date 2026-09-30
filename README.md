# DevOps Copilot

AI incident response agent: FastAPI multi-agent backend (`backend/`, port 8000) + React/Vite dashboard (`frontend/`, port 5173).

Run: `docker compose -f docker-compose.alloy.yaml up`. Set `GEMINI_API_KEY` to use Gemini for diagnosis (falls back to a heuristic engine otherwise). Trigger an incident from the dashboard or `python mock-environment/simulate_incident.py --scenario payment_db_timeout`.
