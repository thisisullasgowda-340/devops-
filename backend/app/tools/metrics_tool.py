from . import deployment_tool
def error_rate(service: str, step: int) -> float:
    if deployment_tool.STATE.get(service) == "v2.4.1":
        return 62.0
    return max(0.0, round(40.0 / (step + 1) - 4, 1))
