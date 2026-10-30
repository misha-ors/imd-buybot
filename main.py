
 http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID", "-1004393947316")
TOKEN_CONTRACT = "TEBhTK13xxVdMoEutByrsQgz9qdpaS6jLZ"
TRONSCAN_API_KEY = os.environ.get("TRONSCAN_API_KEY")
MIN_AMOUNT = 5
PORT = int(os.environ.get("PORT", 10000))
last_tx = None

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def get_transfers():
    url = "https://apilist.tronscanapi.com/api/token_trc20/transfers"
    params = {"limit": 20, "start": 0, "contract_address": TOKEN_CONTRACT}
    headers = {"TRON-PRO-API-KEY": TRONSCAN_API_KEY}
    try:
        r = requests.get(url, params=params, headers=headers, timeout=15)
        data = r.json()
        transfers = data.get("token_transfers", [])
        log(f"://
