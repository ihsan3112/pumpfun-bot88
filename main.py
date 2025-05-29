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
PUMPFUN_API = "https://client-api-2-0.prod.pump.fun/tokens/recent"  # ✅ URL valid
JUPITER_SWAP_API = "https://quote-api.jup.ag/v6/swap"
RPC_URL = "https://api.mainnet-beta.solana.com"
BUY_AMOUNT_SOL = 0.01

# --- Load Wallet ---
with open("my-autobuy-wallet.json") as f:
    secret = json.load(f)
    keypair = Keypair.from_secret_key(bytes(secret))

client = Client(RPC_URL)
ALREADY_BOUGHT = []

# --- Ambil token baru ---
def get_recent_tokens():
    try:
        res = requests.get(PUMPFUN_API)
        print("DEBUG response:", res.status_code)
        print("DEBUG JSON:", res.text[:200])  # tampilkan 200 karakter awal
        tokens = res.json().get("recentTokens", [])
        return [t for t in tokens if t["mint"] not in ALREADY_BOUGHT]
    except Exception as e:
        print("❌ Gagal ambil token:", e)
        return []

# --- Proses beli ---
def beli_token(token):
    print(f"🛒 Membeli token {token['tokenSymbol']} sebesar {BUY_AMOUNT_SOL} SOL... (simulasi)")
    time.sleep(2)
    print(f"✅ Pembelian {token['tokenSymbol']} berhasil.\n")

# --- Loop utama ---
print("🚀 Bot aktif...")
while True:
    tokens = get_recent_tokens()
    if tokens:
        for token in tokens:
            beli_token(token)
            ALREADY_BOUGHT.append(token["mint"])
    else:
        print("⏳ Belum ada token baru. Menunggu 10 detik...\n")
    time.sleep(10)
