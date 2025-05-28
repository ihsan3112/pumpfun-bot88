
from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.publickey import PublicKey
import requests
import json
import base64

# === KONFIGURASI ===
BUY_AMOUNT_SOL = 0.05
TAKE_PROFIT_MULTIPLIER = 2.0
TRAILING_STOP_DROP = 0.3
PUMPFUN_API = "https://api.pump.fun/markets/recent"
RPC = "https://api.mainnet-beta.solana.com"
JUPITER_PRICE_API = "https://price.jup.ag/v4/price?ids="

# === LOAD WALLET ===
with open("my-autobuy-wallet.json", "r") as f:
    secret_key = json.load(f)
    keypair = Keypair.from_secret_key(bytes(secret_key))
    my_address = keypair.public_key

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
        data = res.json()
        return data
    except:
        return {}

print("Bot berhasil dijalankan.")
