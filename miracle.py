
# ===============================

# MIRACLE Ultimate Telegram Bot

# Single-file, Render-ready

# ===============================

 

import os

import time

import requests

from flask import Flask

 

# -------------------------------

# REQUIRED CONFIG (DO NOT REMOVE)

# -------------------------------

 

BOT_TOKEN = "8546621203:AAHUHSge_PtfjFxIITf8_hFUPt9Mfu5YqPE"  

CHANNEL = "@miracle_amazon_deals"

BASE_URL = "https://amazon-click-tracker.onrender.com"

 

PRODUCTS = {

    "Boat Airdopes": "https://amzn.to/4r31I3I",

    "Phoenix Smartwatch": "https://amzn.to/3NTmswf"

}

 

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

 

# -------------------------------

# FLASK APP FOR RENDER

# -------------------------------

 

app = Flask(__name__)

 

@app.route("/")

def home():

    return "✅ MIRACLE Bot is LIVE on Render"

 

# -------------------------------

# TELEGRAM FUNCTIONS

# -------------------------------

 

def send_message(text):

    url = f"{TELEGRAM_API}/sendMessage"

    payload = {

        "chat_id": CHANNEL,

        "text": text,

        "disable_web_page_preview": False

    }

    r = requests.post(url, data=payload)

    print(r.json())

 

def post_all_deals():

    for name, link in PRODUCTS.items():

        message = f"🔥 *{name}*\n\n👉 Buy Now: {link}"

        send_message(message)

        time.sleep(5)

 

# -------------------------------

# AUTO POST LOOP

# -------------------------------

 

def auto_poster():

    while True:

        post_all_deals()

        time.sleep(3600)  # 1 hour gap

 

# -------------------------------

# START EVERYTHING

# -------------------------------

 

if __name__ == "__main__":

    from threading import Thread

 

    Thread(target=auto_poster).start()

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))