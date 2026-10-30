
import requests, time, os, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID", "-1004393947316")
TOKEN = "TEBhTK13xxVdMoEutByrsQgz9qdpaS6jLZ"
PROXY = "TTfvyrAz86hbZk5iDpKD78pqLGgi8C7AAw"
KEY = os.environ.get("TRONSCAN_API_KEY")
PORT = int(os.environ.get("PORT", 10000))
last = None

def log(m):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {m}", flush=True)

def bot():
    global last
    log("Started")
    while True:
        try:
            r = requests.get("https://apilist.tronscanapi.com/api/token_trc20/transfers", params={"limit":5,"start":0,"contract_address":TOKEN}, headers={"TRON-PRO-API-KEY":KEY}, timeout=15)
            txs = r.json().get("token_transfers", [])
            if txs:
                tx = txs[0]
                tid = tx.get("transaction_id")
                if tid and tid != last:
                    last = tid
                    amt = float(tx.get("quant",0)) / 10**int(tx.get("tokenInfo",{}).get("tokenDecimal",6))
                    fr = tx.get("from_address","")
                    to = tx.get("to_address","")
                    log(f"{amt:.0f} {fr[:8]}->{to[:8]}")
                    if amt >= 1:
                        if fr == PROXY:
                            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id":CHAT_ID,"text":f"🟢 Покупка {amt:,.0f} IMD\nhttps://tronscan.org/#/transaction/{tid}","parse_mode":"HTML"}, timeout=10)
                        elif to == PROXY:
                            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id":CHAT_ID,"text":f"🔴 Продажа {amt:,.0f} IMD\nhttps://tronscan.org/#/transaction/{tid}","parse_mode":"HTML"}, timeout=10)
        except Exception as e:
            log(f"Err: {e}")
        time.sleep(20)

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

if __name__ == "__main__":
    threading.Thread(target=bot, daemon=True).start()
    HTTPServer(("0.0.0.0", PORT), H).serve_forever()
