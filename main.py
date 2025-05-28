import requests
import json
import time

# === KONFIGURASI ===
PUMPFUN_API = "https://api.pump.fun/markets/recent"

# === LOAD WALLET ===
with open("my-autobuy-wallet.json", "r") as f:
    wallet_data = json.load(f)
    print("✅ Dompet berhasil dimuat.")

# === AMBIL TOKEN BARU ===
def get_recent_tokens():
    try:
        res = requests.get(PUMPFUN_API)
        print(f"Status Code: {res.status_code}")
        data = res.json()
        return data.get("markets", [])
    except Exception as e:
        print(f"ERROR get_recent_tokens(): {e}")
        return []

# === LOOPING BOT ===
print("🚀 Bot aktif dan memulai loop...\n")

while True:
    tokens = get_recent_tokens()
    if tokens:
        print(f"🟢 Token Terdeteksi: {tokens[0]}")
    else:
        print("🔄 Belum ada token baru...")
    time.sleep(5)
