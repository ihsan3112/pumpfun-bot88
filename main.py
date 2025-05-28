 import requests
import json
import time

print("🚀 Memulai bot...")

# === Load wallet ===
try:
    with open("my-autobuy-wallet.json", "r") as f:
        wallet = json.load(f)
        print("✅ Dompet berhasil dimuat.")
except Exception as e:
    print(f"❌ Gagal memuat dompet: {e}")

# === Ambil token Pump.fun ===
def get_recent_tokens():
    try:
        url = "https://api.pump.fun/markets/recent"
        response = requests.get(url)
        print(f"🌐 Status Code: {response.status_code}")
        data = response.json()
        return data.get("markets", [])
    except Exception as e:
        print(f"❌ ERROR saat ambil token: {e}")
        return []

# === Loop utama ===
while True:
    print("🔁 Mengecek token baru...")
    tokens = get_recent_tokens()

    if tokens:
        print(f"🟢 Token ditemukan: {tokens[0]['name']} - Mint: {tokens[0]['mint']}")
    else:
        print("🔄 Belum ada token baru.")
    
    time.sleep(5)
