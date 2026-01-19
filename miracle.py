# ---------------------- MIRACLE Ultimate Single File ----------------------
# Combines:
# 1. Flask tracker & deal pages
# 2. Click dashboard
# 3. AI-generated captions
# 4. Telegram bot auto-posting
# 5. Affiliate links
# ---------------------------------------------------------------------------

from flask import Flask, redirect, request, render_template_string
import sqlite3
import datetime
import requests
import threading
import time

# ---------------------- CONFIGURATION ----------------------
BOT_TOKEN = "xxxx"                         # Replace with your BotFather token
CHANNEL = "@your_channel_username"         # Replace with your Telegram channel username
BASE_URL = "https://your-render-url"       # Replace with your deployed Render URL

POST_INTERVAL = 3600                       # Seconds between Telegram posts

PRODUCTS = {
    "slug1": "SiteStripe_link1",
    "slug2": "SiteStripe_link2"
}

# ---------------------- FLASK APP ----------------------
app = Flask(__name__)

# SQLite DB setup
db = sqlite3.connect("clicks.db", check_same_thread=False)
db.execute("""
CREATE TABLE IF NOT EXISTS clicks (
    slug TEXT,
    source TEXT,
    ip TEXT,
    time TEXT
)
""")
db.commit()

# ---------------------- ROUTES ----------------------
@app.route("/")
def home():
    return "🚀 MIRACLE Amazon Deals Tracker is running!"

@app.route("/go/<slug>")
def go(slug):
    amazon_link = PRODUCTS.get(slug)
    if not amazon_link:
        return redirect("https://www.amazon.in")

    source = request.args.get("src", "unknown")
    db.execute(
        "INSERT INTO clicks VALUES (?, ?, ?, ?)",
        (slug, source, request.remote_addr, datetime.datetime.now().isoformat())
    )
    db.commit()
    return redirect(amazon_link)

@app.route("/dashboard")
def dashboard():
    rows = db.execute("""
        SELECT slug, source, COUNT(*) as total
        FROM clicks
        GROUP BY slug, source
        ORDER BY total DESC
    """).fetchall()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MIRACLE Tracker</title>
        <style>
            body { font-family: Arial; background: #f2f4f7; padding: 20px; }
            table { width: 100%; background: white; border-collapse: collapse; }
            th, td { padding: 10px; border-bottom: 1px solid #ddd; }
            th { background: #222; color: white; }
        </style>
    </head>
    <body>
    <h2>📊 MIRACLE Click Tracker</h2>
    <table>
        <tr>
            <th>Product</th>
            <th>Source</th>
            <th>Clicks</th>
        </tr>
        {% for r in rows %}
        <tr>
            <td>{{ r[0] }}</td>
            <td>{{ r[1] }}</td>
            <td>{{ r[2] }}</td>
        </tr>
        {% endfor %}
    </table>
    </body>
    </html>
    """
    return render_template_string(html, rows=rows)

@app.route("/deal/<slug>")
def deal(slug):
    link = PRODUCTS.get(slug)
    if not link:
        return redirect("https://www.amazon.in")

    return f"""
    <h2>🔥 Exclusive Deal</h2>
    <p>Limited-time offer on <b>{slug.upper()}</b></p>
    <a href="{link}" target="_blank">
        <button style='padding:15px;font-size:18px'>
            Buy on Amazon
        </button>
    </a>
    """

@app.route("/caption/<slug>")
def caption(slug):
    # Basic AI-generated captions
    captions = {
        "slug1": [
            "🔥 Limited-time deal on this top product!",
            "🕒 Grab it before stock ends!",
            "💎 Perfect for your daily needs!"
        ],
        "slug2": [
            "🎧 Best deal for music lovers!",
            "⚡ Compact, lightweight & powerful",
            "💥 Don’t miss this amazing price!"
        ]
    }
    return {"captions": captions.get(slug, ["💥 Amazing deal – buy now!"])}

# ---------------------- TELEGRAM BOT ----------------------
def get_caption(slug):
    try:
        r = requests.get(f"{BASE_URL}/caption/{slug}")
        r.raise_for_status()
        return "\n".join(r.json().get("captions", ["💥 Grab this deal!"]))
    except:
        return "💥 Grab this deal!"

def post_deal(slug):
    link = f"{BASE_URL}/go/{slug}?src=telegram"
    caption = get_caption(slug)
    text = f"{slug.upper()}\n{caption}\n\n👉 Buy Now: {link}"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHANNEL, "text": text, "disable_web_page_preview": False}
    try:
        res = requests.post(url, data=data)
        if res.status_code == 200:
            print(f"[SUCCESS] Posted {slug} to Telegram")
        else:
            print(f"[FAIL] {res.status_code}: {res.text}")
    except Exception as e:
        print(f"[ERROR] Posting {slug}: {e}")

def telegram_loop():
    print("🚀 Telegram bot started, auto-posting deals...")
    while True:
        for slug in PRODUCTS:
            post_deal(slug)
            time.sleep(POST_INTERVAL)

# ---------------------- MAIN ----------------------
if __name__ == "__main__":
    # Run Telegram bot in a separate thread
    threading.Thread(target=telegram_loop, daemon=True).start()
    # Run Flask server
    app.run(host="0.0.0.0", port=10000)