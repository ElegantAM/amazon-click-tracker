from flask import Flask, redirect, request, render_template
import sqlite3
import datetime

app = Flask(__name__)

# ===============================
# AMAZON AFFILIATE LINKS
# ===============================
LINKS = {
    "phoenix": "https://amzn.to/4jMLDN6",
    "earbuds": "https://amzn.to/4q4nZNL"
}

# ===============================
# DATABASE SETUP
# ===============================
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

# ===============================
# ROUTES
# ===============================
@app.route("/")
def home():
    return "✅ MIRACLE Amazon Click Tracker is LIVE"

@app.route("/go/<slug>")
def go(slug):
    amazon_link = LINKS.get(slug)

    if not amazon_link:
        return redirect("https://www.amazon.in")

    source = request.args.get("src", "unknown")

    db.execute(
        "INSERT INTO clicks VALUES (?, ?, ?, ?)",
        (
            slug,
            source,
            request.remote_addr,
            datetime.datetime.now().isoformat()
        )
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

    return render_template("dashboard.html", rows=rows)

# ===============================
# START SERVER
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)