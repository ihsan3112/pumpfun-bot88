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

# === Konfigurasi ===
PUMPFUN_API = "https://api.pump.fun/markets/recent"
JUPITER_SWAP_API = "https://quote-api.jup.ag/v6/swap"
RPC_URL = "https://api.mainnet-beta.solana.com"
BUY_AMOUNT_SOL = 0.01
TAKE_PROFIT_MULTIPLIER = 2.0
TRAILING_STOP_DROP = 0.3

print("🔄 Memulai bot...")

# === Load Wallet ===
try:
    with open("my-autobuy-wallet.json") as f:
        secret = json.load(f)
        keypair = Keypair.from_secret_key(bytes(secret))
        print("✅ Dompet berhasil dimuat.")
except Exception as e:
    print("❌ Gagal memuat wallet:", e)
    exit()

client = Client(RPC_URL)
ALREADY_BOUGHT = []

# === Ambil Token Baru ===
def get_recent_tokens():
    try:
        res = requests.get(PUMPFUN_API)
        tokens = res.json().get("remarkets", [])
        return [t for t in tokens if t["mint"] not in ALREADY_BOUGHT]
    except Exception as e:
        print("⚠️  Gagal ambil token:", e)
        return []

# === Simulasi Beli Token ===
def simulate_buy(token):
    print(f"\n🪙 Token terbaru: {token['symbol']} ({token['mint']})")
    print(f"💸 Membeli token {token['symbol']} sebesar {BUY_AMOUNT_SOL} SOL...")
    time.sleep(1)
    print(f"✅ Pembelian {token['symbol']} berhasil.\n")

# === Main Loop ===
print("🚀 Bot aktif dan memantau token baru...")

while True:
    tokens = get_recent_tokens()
    if tokens:
        for token in tokens:
            ALREADY_BOUGHT.append(token["mint"])
            simulate_buy(token)
            # logika take profit / trailing stop bisa ditambahkan nanti
            time.sleep(2)
    else:
        print("⏳ Belum ada token baru. Menunggu 10 detik...")
    time.sleep(10)
