from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field
import uuid

class Status(str, Enum):
    INIT = "INIT"; COLLECTING = "COLLECTING"; ANALYZING = "ANALYZING"
    APPROVAL_PENDING = "APPROVAL_PENDING"; REMEDIATING = "REMEDIATING"
    VERIFYING = "VERIFYING"; CLOSED = "CLOSED"; REJECTED = "REJECTED"

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

class Alert(BaseModel):
    service: str = "payment-service"
    endpoint: str = "/api/v1/payments"
    error_code: int = 500
    severity: str = "CRITICAL"
    title: str = "High 500 Error Rate on /api/v1/payments"

class TimelineEvent(BaseModel):
    ts: str = Field(default_factory=now)
    agent: str
    message: str

class Incident(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:8])
    alert: Alert
    status: Status = Status.INIT
    created_at: str = Field(default_factory=now)
    timeline: list[TimelineEvent] = []
    logs: list[str] = []
    deployments: list[dict[str, Any]] = []
    diagnosis: Optional[dict[str, Any]] = None
    action: Optional[dict[str, Any]] = None
    metrics: list[dict[str, Any]] = []
    postmortem: Optional[str] = None
