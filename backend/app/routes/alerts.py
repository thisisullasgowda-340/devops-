from fastapi import APIRouter
from ..models.incident import Alert
from ..agents import supervisor
router = APIRouter(prefix="/api/v1")
@router.post("/alerts")
def ingest(alert: Alert):
    return supervisor.start(alert)
