STATE = {"payment-service": "v2.4.1"}
def recent_deployments(service: str):
    return [{"version": "v2.4.1", "deployed": "3 minutes ago", "author": "ci-bot"},
            {"version": "v2.4.0", "deployed": "2 days ago", "author": "ci-bot"}]
def rollback(service: str, version: str) -> str:
    STATE[service] = version
    return f"Rolled back {service} to {version}"
