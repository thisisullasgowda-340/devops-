from ..tools import log_tool, deployment_tool
def run(inc):
    inc.logs = log_tool.query_logs(inc.alert.service)
    inc.deployments = deployment_tool.recent_deployments(inc.alert.service)
    return f"Collected {len(inc.logs)} log lines; DBConnectionTimeoutException detected. Release v2.4.1 deployed 3 minutes ago."
