from flask import Flask, request
import os
import sys
import traceback
import threading
import time

app = Flask(__name__)

# Global bot status tracker
bot_status = "starting"
bot_error = None

@app.route("/")
def home():
    return "✅ Token Bot Running"

@app.route("/health")
def health():
    return {"status": "ok", "bot": bot_status, "error": bot_error}

@app.route("/debug")
def debug():
    return {
        "env": {
            "TELEGRAM_TOKEN": "set" if os.getenv("TELEGRAM_TOKEN") else "missing",
            "RENDER_EXTERNAL_URL": os.getenv("RENDER_EXTERNAL_URL", "not set"),
            "PORT": os.getenv("PORT", "not set"),
        },
        "bot_status": bot_status,
        "bot_error": bot_error
    }

def start_bot():
    global bot_status, bot_error
    print("[BOT] Starting...", flush=True)
    try:
        from bot import run_bot
        bot_status = "running"
        run_bot()
    except Exception as e:
        bot_status = "crashed"
        bot_error = str(e)
        print(f"[BOT ERROR] {e}", flush=True)
        traceback.print_exc()

if __name__ == "__main__":
    print("[MAIN] Starting Token Launcher Bot...", flush=True)

    # Start bot in NON-DAEMON thread so it survives
    bot_thread = threading.Thread(target=start_bot, daemon=False)
    bot_thread.start()

    # Give bot time to initialize
    time.sleep(3)

    # Start Flask on the Render port
    port = int(os.getenv("PORT", 10000))
    print(f"[MAIN] Flask starting on port {port} | Bot status: {bot_status}", flush=True)

    # threaded=True allows concurrent healthchecks
    app.run(host="0.0.0.0", port=port, threaded=True)
