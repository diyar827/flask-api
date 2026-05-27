import requests
import random

BASE_URL = "http://127.0.0.1:5001"

# Opret ladestandere
chargers = [
    {"location": "København N", "status": "available", "power_kw": 22},
    {"location": "København S", "status": "occupied", "power_kw": 50},
    {"location": "Aarhus C", "status": "available", "power_kw": 22},
    {"location": "Odense", "status": "faulted", "power_kw": 11},
    {"location": "Aalborg", "status": "available", "power_kw": 50},
]

print("Opretter ladestandere...")
for c in chargers:
    r = requests.post(f"{BASE_URL}/chargers/", json=c)
    print(f"Charger: {c['location']} - {r.status_code}")

# Hent alle charger IDs
charger_ids = [c["id"] for c in requests.get(f"{BASE_URL}/chargers/").json()]

# Opret sessioner
print("\nOpretter sessioner...")
statuses = ["completed", "completed", "completed", "active", "failed"]
users = [f"U{str(i).zfill(3)}" for i in range(1, 20)]

for i in range(50):
    session = {
        "charger_id": random.choice(charger_ids),
        "user_id": random.choice(users),
        "energy_kwh": round(random.uniform(5, 60), 2),
        "status": random.choice(statuses)
    }
    r = requests.post(f"{BASE_URL}/sessions/", json=session)
    print(f"Session {i+1}: {r.status_code}")

# Hent alle session IDs
session_ids = [s["id"] for s in requests.get(f"{BASE_URL}/sessions/").json()]

# Opret fakturaer
print("\nOpretter fakturaer...")
for sid in session_ids[:30]:
    invoice = {
        "session_id": sid,
        "amount": round(random.uniform(20, 200), 2),
        "currency": "DKK",
        "status": random.choice(["paid", "paid", "pending", "failed"])
    }
    r = requests.post(f"{BASE_URL}/billing/", json=invoice)
    print(f"Invoice for session {sid}: {r.status_code}")

# Generer telemetri og anomaly data
print("\nGenererer telemetri og anomaly data...")
for charger_id in charger_ids:
    for _ in range(10):
        requests.get(f"{BASE_URL}/telemetry/{charger_id}")
        requests.get(f"{BASE_URL}/maintenance/anomaly/{charger_id}")

print("\nAlt data er oprettet! 🎉")