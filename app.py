from flask import Flask
from bot import run_bot
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Multi-Chain Token Bot Running"

@app.route("/health")
def health():
    from wallet_manager import wallet
    from solana_client import SolanaTrader
    t = SolanaTrader()
    return {
        "status": "ok",
        "solana": wallet.solana_pubkey[:10] + "..." if wallet.solana_pubkey else None,
        "eth": wallet.eth_address[:10] + "..." if wallet.eth_address else None,
        "sol_balance": t.get_sol_balance()
    }

def start_bot():
    run_bot()

if __name__ == "__main__":
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()
    app.run(host="0.0.0.0", port=10000)
