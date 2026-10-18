import requests, time, os, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
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
        log(f"Получено: {len(transfers)}")
        return transfers
    except Exception as e:
        log(f"Ошибка API: {e}")
        return []

def send_msg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}, timeout=10)
        log(f"Отправлено: {r.status_code}")
    except Exception as e:
        log(f"Ошибка отправки: {e}")

def bot_loop():
    global last_tx
    log("Бот запущен")
    while True:
        transfers = get_transfers()
        if transfers:
            tx = transfers[0]
            tx_id = tx.get("transaction_id")
            if tx_id and tx_id != last_tx:
                last_tx = tx_id
                try:
                    quant = float(tx.get("quant", 0))
                    decimals = int(tx.get("tokenInfo", {}).get("tokenDecimal", 6))
                    amount = quant / (10 ** decimals)
                    log(f"Транзакция: {amount:.2f} IMD")
                    if amount >= MIN_AMOUNT:
                        msg = f"🟢 Новая покупка IMD\n\n💰 Сумма: {amount:,.2f} IMD\n🔗 https://tronscan.org/#/transaction/{tx_id}"
                        send_msg(msg)
                except Exception as e:
                    log(f"Ошибка: {e}")
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
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    log(f"Server started on {PORT}")
    server.serve_forever()
    
    import requests
import time
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
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
    params = {
        "limit": 20,
        "start": 0,
        "contract_address": TOKEN_CONTRACT
    }
    headers = {"TRON-PRO-API-KEY": TRONSCAN_API_KEY}
    try:
        r = requests.get(url, params=params, headers=headers, timeout=15)
        data = r.json()
        transfers = data.get("token_transfers", [])
        log(f"Получено транзакций: {len(transfers)}")
        return transfers
    except Exception as e:
        log(f"Ошибка API: {e}")
        return []

def send_msg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }, timeout=10)
        log(f"Сообщение отправлено: {r.status_code}")
    except Exception as e:
        log(f"Ошибка отправки: {e}")

def bot_loop():
    global last_tx
    log("Бот запущен")
    while True:
        transfers = get_transfers()
        if transfers:
            tx = transfers[0]
            tx_id = tx.get("transaction_id")
            if tx_id and tx_id != last_tx:
                last_tx = tx_id
                try:
                    quant = float(tx.get("quant", 0))
                    decimals = int(tx.get("tokenInfo", {}).get("tokenDecimal", 6))
                    amount = quant / (10 ** decimals)
                    log(f"Новая транзакция: {amount:.2f} IMD")
                    if amount >= MIN_AMOUNT:
                        msg = (
                            f"🟢 Новая покупка IMD\n\n"
                            f"💰 Сумма: {amount:,.2f} IMD\n"
                            f"🔗 Транзакция: https://tronscan.org/#/transaction/{tx_id}"
                        )
                        send_msg(msg)
                    else:
                        log(f"Сумма {amount:.2f} меньше минимума")
                except Exception as e:
                    log(f"Ошибка обработки: {e}")
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
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    log(f"Web server started on port {PORT}")
    server.serve_forever()
