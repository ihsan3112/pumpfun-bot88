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
PUMPFUN_API = "https://api.pump.fun/markets/recent"
JUPITER_SWAP_API = "https://quote-api.jup.ag/v6/swap"
RPC_URL = "https://api.mainnet-beta.solana.com"
BUY_AMOUNT_SOL = 0.01

# --- Load Wallet ---
with open("my-autobuy-wallet.json") as f:
    secret = json.load(f)
    keypair = Keypair.from_secret_key(bytes(secret))

client = Client(RPC_URL)
ALREADY_BOUGHT = []

def get_recent_tokens():
    try:
        res = requests.get(PUMPFUN_API)
        tokens = res.json().get("remarkets", [])
        return [t for t in tokens if t["mint"] not in ALREADY_BOUGHT]
    except Exception as e:
        print(f"❌ Gagal ambil token: {e}")
        return []

def swap_token(to_mint):
    try:
        print(f"🛒 Siap beli token: {to_mint}")
        params = {
            "inputMint": "So11111111111111111111111111111111111111112",  # SOL
            "outputMint": to_mint,
            "amount": str(int(BUY_AMOUNT_SOL * 10**9)),  # dalam lamports
            "slippage": 3,
            "userPublicKey": str(keypair.public_key),
            "wrapUnwrapSOL": True,
            "feeBps": 0
        }

        # Ambil route transaksi swap
        swap_req = requests.post(JUPITER_SWAP_API, json=params).json()
        if "swapTransaction" not in swap_req:
            print("⚠️ Gagal ambil transaksi swap.")
            return False

        # Decode base64 -> transaction
        swap_tx = base64.b64decode(swap_req["swapTransaction"])
        txn = Transaction.deserialize(swap_tx)
        txn.sign([keypair])

        # Kirim ke jaringan
        txid = client.send_transaction(txn, keypair, opts=TxOpts(skip_preflight=True, preflight_commitment="confirmed"))
        print(f"✅ Transaksi terkirim: https://solscan.io/tx/{txid['result']}")
        return True
    except Exception as e:
        print(f"❌ Gagal beli token: {e}")
        return False

# === Loop utama ===
while True:
    tokens = get_recent_tokens()
    for token in tokens:
        mint = token["mint"]
        name = token.get("name", "TokenBaru")
        if mint in ALREADY_BOUGHT:
            continue
        print(f"\n🆕 Token baru: {name} | Mint: {mint}")

        success = swap_token(mint)
        if success:
            ALREADY_BOUGHT.append(mint)
            time.sleep(10)
    time.sleep(5)
