import time
import random

BUY_AMOUNT_SOL = 0.01
TOKENS_DUMMY = ["TokenA", "TokenB", "TokenC", "TokenD", "TokenE"]

print("Bot dummy aktif.")

while True:
    token = random.choice(TOKENS_DUMMY)
    print(f"Token terbaru: {token}")
    print(f"🛒 Membeli token {token} sejumlah {BUY_AMOUNT_SOL} SOL...")
    
    time.sleep(2)
    print(f"✅ Pembelian {token} berhasil.\n")
    time.sleep(3)
