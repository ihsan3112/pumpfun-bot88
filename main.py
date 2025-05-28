import time
import random
import requests
import json

# ======== KONFIGURASI =========
BUY_AMOUNT_SOL = 0.01
TOKENS_DUMMY = ["TokenA", "TokenB", "TokenC", "TokenD", "TokenE"]

# Telegram config
TELEGRAM_ENABLED = True
BOT_TOKEN = "8161302162:AAFyas7aBR1r3X-HaznMwWhuhfV2jZfqDHCA"
CHAT_ID = "78066164019"

def send_telegram(message):
    if TELEGRAM_ENABLED:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": message
        }
        try:
            requests.post(url, data=data)
        except Exception as e:
            print(f"Gagal kirim pesan Telegram: {e}")

print("🤖 Bot dummy aktif...")

while True:
    token = random.choice(TOKENS_DUMMY)
    print(f"🆕 Token terbaru: {token}")
    print(f"💰 Membeli token {token} sejumlah {BUY_AMOUNT_SOL} SOL...")
    send_telegram(f"🆕 Token baru terdeteksi: {token}\n💰 Membeli {BUY_AMOUNT_SOL} SOL")

    time.sleep(2)
    print(f"✅ Pembelian {token} berhasil.\n")
    send_telegram(f"✅ Pembelian token {token} berhasil.")
    time.sleep(5)
