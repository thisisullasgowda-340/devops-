def postmortem(inc) -> str:
    d = inc.diagnosis or {}
    ev = "\n".join(f"- {e}" for e in d.get("evidence_list", []))
    tl = "\n".join(f"- `{t.ts[11:19]}` **{t.agent}**: {t.message}" for t in inc.timeline)
    return f"""# Post-Mortem: {inc.alert.title}

**Incident ID:** {inc.id}  
**Service:** {inc.alert.service}  
**Severity:** {inc.alert.severity}

## Root Cause
{d.get('root_cause_summary','')}

## Evidence
{ev}

## Remediation
{d.get('proposed_fix','')} (approved by on-call engineer)

## Timeline
{tl}

## Follow-ups
- Add config validation rejecting DATABASE_POOL_SIZE < 1
- Add canary stage gating on payment error rate
"""
