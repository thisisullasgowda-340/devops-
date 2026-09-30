from fastapi import APIRouter, HTTPException
from ..agents import supervisor
router = APIRouter(prefix="/api/v1/incidents")
@router.get("")
def list_incidents():
    return sorted(supervisor.INCIDENTS.values(), key=lambda i: i.created_at, reverse=True)
@router.get("/{iid}")
def get(iid: str):
    if iid not in supervisor.INCIDENTS: raise HTTPException(404)
    return supervisor.INCIDENTS[iid]
@router.post("/{iid}/approve")
def approve(iid: str):
    if iid not in supervisor.INCIDENTS: raise HTTPException(404)
    return supervisor.decide(iid, True)
@router.post("/{iid}/reject")
def reject(iid: str):
    if iid not in supervisor.INCIDENTS: raise HTTPException(404)
    return supervisor.decide(iid, False)
