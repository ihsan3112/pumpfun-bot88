import requests
import json
import time

print("🚀 Bot mulai...")

# === Load wallet ===
with open("my-autobuy-wallet.json", "r") as f:
    wallet = json.load(f)
    print("✅ Dompet berhasil dimuat.")

# === Ambil token baru ===
def get_recent_tokens():
    try:
        res = requests.get("https://api.pump.fun/markets/recent")
        print(f"Status Code: {res.status_code}")
        return res.json().get("markets", [])
    except Exception as e:
        print(f"❌ ERROR saat fetch token: {e}")
        return []

# === Loop utama ===
while True:
    tokens = get_recent_tokens()
    if tokens:
        print(f"🟢 Terdeteksi token: {tokens[0]}")
    else:
        print("🔄 Tidak ada token baru.")
    time.sleep(5)
