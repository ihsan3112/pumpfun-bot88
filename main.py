import requests
import json

# === KONFIGURASI ===
BUY_AMOUNT_SOL = 0.05
TAKE_PROFIT_MULTIPLIER = 2.0
TRAILING_STOP_DROP = 0.3
PUMPFUN_API = "https://api.pump.fun/markets/recent"
JUPITER_PRICE_API = "https://price.jup.ag/v4/price?ids="

# === LOAD WALLET ===
with open("my-autobuy-wallet.json", "r") as f:
    wallet_data = json.load(f)
    print("Dompet berhasil dimuat.")

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

print("Bot aktif. Token terbaru:", get_recent_tokens()[:1])
