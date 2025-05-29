import time
import json
import requests
from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.rpc.types import TxOpts
from solana.transaction import Transaction
from solders.pubkey import Pubkey
from solders.signature import Signature
import base64

# --- Konfigurasi ---
PUMPFUN_API = "https://api.pump.fun/api/tokens/recent"
JUPITER_SWAP_API = "https://quote-api.jup.ag/v6/swap"
RPC_URL = "https://api.mainnet-beta.solana.com"
BUY_AMOUNT_SOL = 0.01

# --- Load Wallet ---
with open("my-autobuy-wallet.json") as f:
    secret = json.load(f)
    keypair = Keypair.from_secret_key(bytes(secret))

client = Client(RPC_URL)
ALREADY_BOUGHT = []

# --- Ambil token dari Pump.fun ---
def get_recent_tokens():
    try:
        res = requests.get(PUMPFUN_API)
        tokens = res.json().get("tokens", [])
        return [t for t in tokens if t["mint"] not in ALREADY_BOUGHT]
    except Exception as e:
        print("❌ Gagal ambil token:", e)
        return []

# --- Dummy auto-buy logic (untuk demo) ---
def auto_buy():
    while True:
        tokens = get_recent_tokens()
        if tokens:
            for token in tokens:
                mint = token["mint"]
                print(f"🪙 Token terbaru: {mint}")
                print(f"🛒 Membeli token {mint} sebesar {BUY_AMOUNT_SOL} SOL...")
                # (Simulasi pembelian. Belum real tx karena belum swap & sign)
                time.sleep(2)
                print(f"✅ Pembelian token {mint} berhasil.\n")
                ALREADY_BOUGHT.append(mint)
        else:
            print("⏳ Belum ada token baru. Menunggu 10 detik...\n")
        time.sleep(10)

if __name__ == "__main__":
    print("🤖 Bot aktif.")
    auto_buy()
