from flask import Flask, redirect, request, render_template_string
import sqlite3
import datetime
import os

app = Flask(__name__)

# -----------------------------
# AMAZON AFFILIATE LINKS
# Paste your SiteStripe links here
# -----------------------------
LINKS = {
    "phoenix": "https://amzn.to/4jMLDN6",
    "earbuds": "https://amzn.to/4q4nZNL"
    "trimmer":
"https://amzn.to/3NkycIb"
}

# -----------------------------
# DATABASE SETUP
# -----------------------------
DB_FILE = "clicks.db"

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clicks (
            slug TEXT,
            source TEXT,
            ip TEXT,
            time TEXT
        )
    """)
    conn.commit()
    return conn

# -----------------------------
# ROUTES
# -----------------------------
@app.route("/")
def home():
    return "✅ Amazon Click Tracker is LIVE"

@app.route("/go/<slug>")
def go(slug):
    amazon_link = LINKS.get(slug)

    if amazon_link is None:
        return redirect("https://www.amazon.in")

    source = request.args.get("src", "direct")
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)

    conn = get_db()
    conn.execute(
        "INSERT INTO clicks VALUES (?, ?, ?, ?)",
        (
            slug,
            source,
            ip,
            datetime.datetime.now().isoformat()
        )
    )
    conn.commit()
    conn.close()

    return redirect(amazon_link)

@app.route("/dashboard")
def dashboard():
    conn = get_db()
    rows = conn.execute("""
        SELECT slug, source, COUNT(*) AS total
        FROM clicks
        GROUP BY slug, source
        ORDER BY total DESC
    """).fetchall()
    conn.close()

    html = """
    <h2>📊 Amazon Click Dashboard</h2>
    <table border="1" cellpadding="8">
        <tr>
            <th>Product</th>
            <th>Source</th>
            <th>Clicks</th>
        </tr>
        {% for row in rows %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
        </tr>
        {% endfor %}
    </table>
    """

    return render_template_string(html, rows=rows)

# -----------------------------
# START SERVER
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)