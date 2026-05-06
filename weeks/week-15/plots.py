import re
import pandas as pd
import matplotlib.pyplot as plt

with open("logs.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

blocks = raw_text.split("Running 30s test")

data = []

for block in blocks:
    conn = re.search(r"(\d+) connections", block)
    lat = re.search(r"Latency\s+([\d\.]+)ms\s+([\d\.]+)ms\s+([\d\.]+)(ms|s)", block)
    req = re.search(r"Req/Sec\s+([\d\.]+)\s+([\d\.]+)\s+([\d\.]+)", block)
    total = re.search(r"(\d+) requests", block)
    rps = re.search(r"Requests/sec:\s+([\d\.]+)", block)
    tr = re.search(r"Transfer/sec:\s+([\d\.]+)KB", block)

    if not all([conn, lat, req, total, rps, tr]):
        continue

    connections = int(conn.group(1))
    latency_avg = float(lat.group(1))
    latency_std = float(lat.group(2))
    latency_max = float(lat.group(3)) * (1000 if lat.group(4) == 's' else 1)

    req_avg = float(req.group(1))
    req_std = float(req.group(2))
    req_max = float(req.group(3))

    total_requests = int(total.group(1))
    requests_per_sec = float(rps.group(1))
    transfer_per_sec = float(tr.group(1))

    data.append({
        "connections": connections,
        "latency_avg_ms": latency_avg,
        "latency_std_ms": latency_std,
        "latency_max_ms": latency_max,
        "req_per_thread_avg": req_avg,
        "req_per_thread_std": req_std,
        "req_per_thread_max": req_max,
        "total_requests": total_requests,
        "requests_per_sec": requests_per_sec,
        "transfer_kb_sec": transfer_per_sec,
    })

df = pd.DataFrame(data)

if df.empty:
    raise ValueError("Парсер ничего не нашёл — проверь файл logs.txt")

df = df.sort_values("connections")

print(df)

plt.figure()
plt.plot(df["connections"], df["requests_per_sec"], marker='o')
plt.xlabel("Connections")
plt.ylabel("Requests/sec")
plt.title("Throughput vs Connections")
plt.grid()

plt.figure()
plt.plot(df["connections"], df["latency_avg_ms"], marker='o', label="avg")
plt.plot(df["connections"], df["latency_max_ms"], marker='o', label="max")
plt.xlabel("Connections")
plt.ylabel("Latency (ms)")
plt.title("Latency vs Connections")
plt.legend()
plt.grid()

plt.figure()
plt.plot(df["connections"], df["transfer_kb_sec"], marker='o')
plt.xlabel("Connections")
plt.ylabel("KB/sec")
plt.title("Transfer Rate vs Connections")
plt.grid()

plt.show()