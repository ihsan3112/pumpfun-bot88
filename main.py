import requests
import json
import time

print("🚀 Bot dimulai...")

# === Load wallet ===
try:
    with open("my-autobuy-wallet.json", "r") as f:
        wallet = json.load(f)
        print("✅ Dompet berhasil dimuat.")
except Exception as e:
    print(f"❌ Gagal memuat dompet: {e}")

# === Ambil token Pump.fun ===
import random
import string
import time
def get_recent_tokens():
    try:
        url = "https://api.pump.fun/api/markets/recent"
        response = requests.get(url)
        print(f"🌐 Status: {response.status_code}")
        data = response.json()
        return data.get("markets", [])
    except Exception as e:
        print(f"❌ Error ambil token: {e}")
        return []

# === Loop aktif ===
while True:
    print("🔄 Mengecek token baru...")
    tokens = get_recent_tokens()

    if tokens:
        print(f"🟢 Token: {tokens[0]['name']} | Mint: {tokens[0]['mint']}")
    else:
        print("⏳ Belum ada token.")

    time.sleep(5)
