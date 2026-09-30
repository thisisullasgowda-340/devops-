def query_logs(service: str) -> list[str]:
    base = "2026-09-30T13:4"
    lines = [f"{base}0:01Z INFO  {service} request POST /api/v1/payments 200 42ms"]
    for i in range(2, 12):
        lines.append(f"{base}{i//10}:{i:02d}Z ERROR {service} DBConnectionTimeoutException: pool exhausted (size=0) after 5000ms")
        if i % 3 == 0:
            lines.append(f"{base}{i//10}:{i:02d}Z WARN  {service} retrying transaction txn_{1000+i}")
    return lines
