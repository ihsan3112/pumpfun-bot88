import time
import json
import requests
import random
from solana.rpc.api import Client
from solana.keypair import Keypair

# === Config ===
PUMPFUN_API = "https://api.pump.fun/api/tokens/recent"
RPC_URL = "https://api.mainnet-beta.solana.com"
BUY_AMOUNT_SOL = 0.01

# === Load Wallet ===
with open("my-autobuy-wallet.json", "r") as f:
    secret = json.load(f)
    keypair = Keypair.from_secret_key(bytes(secret))

client = Client(RPC_URL)
ALREADY_BOUGHT = []

# === Generate acak interval 3 jam ===
def generate_delays():
    pola_awal = [1, 2, 3, 5, 10]  # menit
    jam1 = pola_awal + pola_awal[::-1]
    jam2 = [x * 2 for x in jam1]
    jam3 = jam1
    semua = jam1 + jam2 + jam3
    return [x * 60 for x in semua]  # detik

DELAY_SEQUENCE = generate_delays()
delay_index = 0

# === Ambil token baru dari Pump.fun ===
def get_new_tokens():
    try:
        res = requests.get(PUMPFUN_API, timeout=10)
        tokens = res.json().get("tokens", [])
        return [t for t in tokens if t["mint"] not in ALREADY_BOUGHT]
    except Exception as e:
        print("❌ Error ambil token:", e)
        return []

# === Simulasi beli ===
def dummy_autobuy():
    global delay_index
    delay_time = DELAY_SEQUENCE[delay_index % len(DELAY_SEQUENCE)]
    print(f"\n⏳ Tunggu {delay_time//60} menit sebelum ambil token berikutnya...\n")
    time.sleep(delay_time)

    tokens = get_new_tokens()
    if tokens:
        for token in tokens:
            mint = token["mint"]
            print(f"🪙 Token baru: {mint}")
            print(f"🛒 Beli dummy {BUY_AMOUNT_SOL} SOL...")
            time.sleep(1)
            print(f"✅ Dummy beli token {mint} selesai!\n")
            ALREADY_BOUGHT.append(mint)
            break  # hanya beli 1 token per siklus
    else:
        print("📭 Tidak ada token baru.")

    delay_index += 1

# === Main ===
if __name__ == "__main__":
    print("🤖 Bot dimulai...")
    while True:
        dummy_autobuy()
