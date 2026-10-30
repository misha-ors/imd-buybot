LAUNCHPAD_PROXY = "TTfvy rAz86hbZk5iDpKD78pqLGgi8C7AAw"
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
    log("Б
