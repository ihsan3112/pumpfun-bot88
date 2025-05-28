from solana.rpc.api import Client
from solana.publickey import PublicKey
import requests
import json

# === KONFIGURASI ===
BUY_AMOUNT_SOL = 0.05
TAKE_PROFIT_MULTIPLIER = 2.0
TRAILING_STOP_DROP = 0.3
PUMPFUN_API = "https://api.pump.fun/markets/recent"
RPC = "https://api.mainnet-beta.solana.com"
JUPITER_PRICE_API = "https://price.jup.ag/v4/price?ids="

# === LOAD WALLET ===
with open("my-autobuy-wallet.json", "r") as f:
    key = json.load(f)
    pubkey_bytes = key[32:]  # Ambil 32 byte terakhir (public key)
    my_address = PublicKey(pubkey_bytes)

client = Client(RPC)
sudah_beli = {}

# === AMBIL TOKEN BARU ===
def get_recent_tokens():
    try:
        res = requests.get(PUMPFUN_API).json()
        return res["markets"]
    except:
        return []

# === AMBIL HARGA TOKEN ===
def get_token_price(token_mint):
    try:
        res = requests.get(f"{JUPITER_PRICE_API}{token_mint}")
        return res.json()
    except:
        return {}

print("Bot berhasil dijalankan. Alamat dompet:", my_address)
