import argparse, json, urllib.request
p = argparse.ArgumentParser(); p.add_argument("--scenario", default="payment_db_timeout")
p.add_argument("--api", default="http://localhost:8000")
a = p.parse_args()
req = urllib.request.Request(f"{a.api}/api/v1/alerts", method="POST", headers={"Content-Type": "application/json"},
                             data=json.dumps({"service": "payment-service"}).encode())
print(json.load(urllib.request.urlopen(req))["id"])
