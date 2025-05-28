import time
import random

TOKENS = ["TokenA", "TokenB", "TokenC", "TokenD", "TokenE"]

print("🚀 Bot dummy aktif...")

while True:
    token = random.choice(TOKENS)
    print(f"🆕 Token terbaru: {token}")
    print(f"🛒 Membeli token {token} sebesar 0.01 SOL...")
    time.sleep(2)
    print(f"✅ Pembelian {token} berhasil.\n")
    time.sleep(3)
