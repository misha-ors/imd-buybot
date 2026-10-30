
import time, os, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

PORT = int(os.environ.get("PORT", 10000))

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def bot_loop():
    log("Bot started")
    while True:
        log("Bot is alive")
        time.sleep(30)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

if __name__ == "__main__":
    threading.Thread(target=bot_loop, daemon=True).start()
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
