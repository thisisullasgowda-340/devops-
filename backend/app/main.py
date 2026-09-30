from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import alerts, incidents
app = FastAPI(title="DevOps Copilot")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(alerts.router); app.include_router(incidents.router)
@app.get("/health")
def health(): return {"status": "ok"}
