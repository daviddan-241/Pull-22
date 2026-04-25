from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Token Bot Running"

@app.route("/health")
def health():
    return {"status": "ok"}

def start_bot():
    try:
        from bot import run_bot
        run_bot()
    except Exception as e:
        print(f"[BOT ERROR] {e}")
        print("[BOT ERROR] Bot failed, but Flask is running")

if __name__ == "__main__":
    import threading
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()
    app.run(host="0.0.0.0", port=10000)
