import time
import json
import requests
from solana.keypair import Keypair
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from solana.transaction import Transaction
from solders.pubkey import Pubkey
from solders.signature import Signature
import base64

# === Konfigurasi ===
PUMPFUN_API = "https://api.pump.fun/markets/recent"
JUPITER_PRICE_API = "https://price.jup.ag/v4/price"
RPC_URL = "https://api.mainnet-beta.solana.com"
BUY_AMOUNT_SOL = 0.01
TAKE_PROFIT_MULTIPLIER = 2.0
TRAILING_STOP_DROP = 0.3

# === Load Wallet ===
with open("my-autobuy-wallet.json") as f:
    secret = json.load(f)
    keypair = Keypair.from_secret_key(bytes(secret))

client = Client(RPC_URL)
already_bought = []

def get_recent_tokens():
    try:
        res = requests.get(PUMPFUN_API)
        tokens = res.json().get("remarkets", [])
        return [t for t in tokens if t["mint"] not in already_bought]
    except Exception as e:
        print(f"❌ Gagal ambil token: {e}")
        return []

def get_token_price(token_mint):
    try:
        url = f"{JUPITER_PRICE_API}?ids={token_mint}"
        res = requests.get(url)
        return res.json().get(token_mint, {}).get("price", 0)
    except:
        return 0

def simulate_buy_sell(token):
    token_mint = token["mint"]
    name = token["name"]
    already_bought.append(token_mint)
    print(f"🚀 Token terbaru: {name}")
    print(f"🛒 Membeli token {name} sebesar {BUY_AMOUNT_SOL} SOL...")

    buy_price = get_token_price(token_mint)
    peak_price = buy_price
    print(f"💰 Harga beli: {buy_price}")

    while True:
        current_price = get_token_price(token_mint)
        if current_price > peak_price:
            peak_price = current_price

        if current_price >= buy_price * TAKE_PROFIT_MULTIPLIER:
            print(f"✅ Target profit tercapai di harga {current_price}. Jual token {name}.")
            break

        if current_price < peak_price * (1 - TRAILING_STOP_DROP):
            print(f"📉 Trailing stop triggered. Harga turun dari {peak_price} ke {current_price}. Jual token {name}.")
            break

        print(f"⏳ Harga saat ini: {current_price}. Menunggu...")
        time.sleep(5)

if __name__ == "__main__":
    print("🤖 Bot aktif...")
    while True:
        tokens = get_recent_tokens()
        for token in tokens:
            simulate_buy_sell(token)
        time.sleep(10)
