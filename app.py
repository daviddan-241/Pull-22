from flask import Flask, request
import os
import sys
import traceback
import threading
import time

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Token Bot Running"

@app.route("/health")
def health():
    return {"status": "ok", "bot": bot_status}

@app.route("/debug")
def debug():
    return {
        "env": {
            "TELEGRAM_TOKEN": "set" if os.getenv("TELEGRAM_TOKEN") else "missing",
            "RENDER_EXTERNAL_URL": os.getenv("RENDER_EXTERNAL_URL", "not set"),
        },
        "bot_status": bot_status
    }

# Global status tracker
bot_status = "starting"

def start_bot():
    global bot_status
    print("[BOT] Starting...", flush=True)
    try:
        from bot import run_bot
        bot_status = "running"
        run_bot()
    except Exception as e:
        bot_status = f"error: {str(e)}"
        print(f"[BOT ERROR] {e}", flush=True)
        traceback.print_exc()

if __name__ == "__main__":
    import threading
    print("[MAIN] Starting...", flush=True)

    # Start bot in NON-DAEMON thread so it stays alive
    bot_thread = threading.Thread(target=start_bot, daemon=False)
    bot_thread.start()

    # Give bot time to initialize before starting Flask
    time.sleep(2)

    # Start Flask on the Render port
    port = int(os.getenv("PORT", 10000))
    print(f"[MAIN] Flask starting on port {port}", flush=True)

    # Use threaded=True so healthchecks don't block
    app.run(host="0.0.0.0", port=port, threaded=True)
