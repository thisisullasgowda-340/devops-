import threading, time
from ..config import STEP_DELAY
from ..models.incident import Incident, Status, TimelineEvent
from ..tools import deployment_tool, metrics_tool
from . import collector, analyzer, guard, reporter

INCIDENTS: dict[str, Incident] = {}
_approvals: dict[str, threading.Event] = {}

def _log(inc, agent, msg):
    inc.timeline.append(TimelineEvent(agent=agent, message=msg))

def _run(inc: Incident):
    _log(inc, "Supervisor", f"Alert received: {inc.alert.severity} - {inc.alert.title}")
    time.sleep(STEP_DELAY)
    inc.status = Status.COLLECTING; _log(inc, "Collector", "Fetching logs, deployments and diffs...")
    time.sleep(STEP_DELAY); _log(inc, "Collector", collector.run(inc))
    inc.status = Status.ANALYZING; _log(inc, "Analyzer", "Correlating telemetry with release changes...")
    time.sleep(STEP_DELAY); _log(inc, "Analyzer", analyzer.run(inc))
    _log(inc, "Guard", guard.classify(inc)); inc.status = Status.APPROVAL_PENDING
    ev = _approvals[inc.id]; ev.wait()
    if inc.action.get("approved") is False:
        inc.status = Status.REJECTED; _log(inc, "Guard", "Remediation rejected by human operator."); return
    inc.status = Status.REMEDIATING
    _log(inc, "Guard", deployment_tool.rollback(inc.alert.service, inc.action["target"]))
    inc.status = Status.VERIFYING; _log(inc, "Verifier", "Polling /health metrics...")
    for i in range(10):
        rate = metrics_tool.error_rate(inc.alert.service, i)
        inc.metrics.append({"t": i, "error_rate": rate}); time.sleep(STEP_DELAY / 3)
    _log(inc, "Verifier", "Error rate returned to 0%. Service healthy.")
    inc.postmortem = reporter.postmortem(inc)
    inc.status = Status.CLOSED; _log(inc, "Reporter", "Post-mortem generated. Incident closed.")

def start(alert) -> Incident:
    deployment_tool.STATE[alert.service] = "v2.4.1"
    inc = Incident(alert=alert); INCIDENTS[inc.id] = inc
    _approvals[inc.id] = threading.Event()
    threading.Thread(target=_run, args=(inc,), daemon=True).start()
    return inc

def decide(iid: str, approved: bool) -> Incident:
    inc = INCIDENTS[iid]
    if inc.status == Status.APPROVAL_PENDING:
        inc.action["approved"] = approved; _approvals[iid].set()
    return inc
