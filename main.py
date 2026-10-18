import requests
import time
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID", "-1004393947316")
TOKEN_CONTRACT = "TEBhTK13xxVdMoEutByrsQgz9qdpaS6jLZ"
TRONSCAN_API_KEY = os.environ.get("TRONSCAN_API_KEY")
MIN_AMOUNT = 5
PORT = int(os.environ.get("PORT", 10000))

last_tx = None

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
        return data.get("token_transfers", [])
    except Exception as e:
        print("Ошибка API:", e)
        return []

def send_msg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }, timeout=10)
        print("Сообщение отправлено")
    except Exception as e:
        print("Ошибка отправки:", e)

def bot_loop():
    global last_tx
    print("Бот запущен")
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
                    if amount >= MIN_AMOUNT:
                        msg = (
                            f"🟢 Новая покупка IMD\n\n"
                            f"💰 Сумма: {amount:,.2f} IMD\n"
                            f"🔗 Транзакция: https://tronscan.org/#/transaction/{tx_id}"
                        )
                        send_msg(msg)
                except Exception as e:
                    print("Ошибка обработки:", e)
        time.sleep(30)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

if __name__ == "__main__":
    # Запускаем бота в отдельном потоке
    threading.Thread(target=bot_loop, daemon=True).start()
    # Запускаем простой веб-сервер, чтобы Render не останавливал процесс
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Web server started on port {PORT}")
    server.serve_forever()
