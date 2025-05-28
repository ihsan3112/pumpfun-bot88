import requests
import time

# Konfigurasi
BUY_AMOUNT_SOL = 0.01
TAKE_PROFIT_MULTIPLIER = 2.0
TRAILING_STOP_DROP = 0.3

PUMPFUN_API = "https://api.pump.fun/markets/recent"
JUPITER_PRICE_API = "https://price.jup.ag/v4/price"

sudah_beli = []

def get_recent_tokens():
    try:
        res = requests.get(PUMPFUN_API)
        return res.json().get("markets", [])
    except:
        return []

def get_token_price(token_mint):
    try:
        res = requests.get(f"{JUPITER_PRICE_API}?ids={token_mint}")
        data = res.json()
        return data.get(token_mint, {}).get("price", 0)
    except:
        return 0

while True:
    print("🔄 Mengecek token baru...")
    tokens = get_recent_tokens()
    for token in tokens:
        mint = token["mint"]
        if mint in sudah_beli:
            continue

        price = get_token_price(mint)
        if price == 0:
            continue

        print(f"✅ Token baru terdeteksi: {mint}")
        print(f"💰 Membeli token {mint} senilai {BUY_AMOUNT_SOL} SOL...")
        sudah_beli.append(mint)

        buy_price = price
        peak_price = price

        while True:
            time.sleep(5)
            current_price = get_token_price(mint)
            if current_price > peak_price:
                peak_price = current_price

            profit_target = buy_price * TAKE_PROFIT_MULTIPLIER
            stop_price = peak_price * (1 - TRAILING_STOP_DROP)

            if current_price >= profit_target:
                print(f"🎯 TAKE PROFIT {mint}: {current_price:.4f} SOL (beli: {buy_price:.4f})")
                break
            elif current_price <= stop_price:
                print(f"🛑 STOP LOSS {mint}: {current_price:.4f} SOL (peak: {peak_price:.4f})")
                break
    time.sleep(10)
