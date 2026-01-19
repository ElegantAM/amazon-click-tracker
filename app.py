from flask import Flask, request, redirect, jsonify
import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return "Amazon Click Tracker is LIVE ✅"

@app.route("/track")
def track():
    asin = request.args.get("asin", "unknown")
    tag = request.args.get("tag", "yourtag-21")

    # Log click (Render logs will store this)
    print(f"CLICK | ASIN: {asin} | TAG: {tag} | TIME: {datetime.datetime.now()}")

    amazon_url = f"https://www.amazon.in/dp/{asin}?tag={tag}"
    return redirect(amazon_url)

@app.route("/health")
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
