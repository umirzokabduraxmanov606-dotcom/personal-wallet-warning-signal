from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# 1) Known exchange / safe addresses (demo)
EXCHANGE_ADDRESSES = {
    "0x1111111111111111111111111111111111111111": "Demo CEX (Ethereum)",
    "TXXXXEXCHANGEADDRESSDEMO111": "Demo TRON Exchange",
}

# 2) Scam / suspicious addresses (demo)
SCAM_ADDRESSES = {
    "0x9999999999999999999999999999999999999999": "Telegram scam wallet",
    "TSCAMWALLETSAMPLE1111111111111": "TRON investment fraud",
}

PAGE = """
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>Personal Wallet Warning Signal</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f3f4f6;
            display: flex;
            justify-content: center;
            padding: 40px 10px;
        }
        .card {
            background: #fff;
            max-width: 640px;
            width: 100%;
            padding: 25px 30px 30px;
            border-radius: 14px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        }
        h1 { margin-top: 0; font-size: 26px; }
        p.subtitle { color: #555; margin-top: 4px; margin-bottom: 20px; }
        form input[type=text] {
            width: 100%; padding: 12px; font-size: 15px;
            border: 1px solid #d1d5db; border-radius: 8px; outline: none;
        }
        form button {
            margin-top: 14px; background: #4f46e5; color: #fff;
            border: none; padding: 10px 18px; border-radius: 8px;
            cursor: pointer; font-size: 14px;
        }
        form button:hover { background: #4338ca; }
        .result {
            margin-top: 20px; padding: 14px 14px 14px 38px;
            border-radius: 10px; position: relative;
        }
        .result::before {
            position: absolute; left: 12px; top: 12px;
        }
        .res-bad   { background: #fee2e2; border: 1px solid #ef4444; }
        .res-bad::before { content: "❌"; }
        .res-warn  { background: #fef3c7; border: 1px solid #fbbf24; }
        .res-warn::before { content: "⚠"; }
        .res-ok    { background: #dcfce7; border: 1px solid #22c55e; }
        .res-ok::before { content: "✅"; }
        .small { margin-top: 18px; font-size: 12px; color: #6b7280; }
        .tag { display: inline-block; padding: 2px 8px; background: #e0ecff; border-radius: 9999px; font-size: 11px; margin-left: 6px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🔐 Personal Wallet Warning Signal</h1>
        <p class="subtitle">
            Enter a wallet address — the system will check it against known scam lists, exchange addresses, and basic validation rules.
        </p>
        <form method="POST">
            <label>Wallet address:</label><br>
            <input type="text" name="address" placeholder="0x..., T..., bc1..." required value="{{ addr or '' }}">
            <button type="submit">Check</button>
        </form>

        {% if message %}
            <div class="result {{ css_class }}">
                {{ message }}
            </div>
        {% endif %}

        <p class="small">
            Demo version. You can connect this list to an API or live database for automatic updates.<br>
            <b>Owner:</b> Umirzok Mamatmurodovich Abduraxmanov <span class="tag">PWWS</span>
        </p>
    </div>
</body>
</html>
"""

def basic_heuristic(a: str):
    if a.startswith("T") and len(a) > 20:
        return "warn", f"{a} — Possible personal wallet (TRON network, EOA). Confirm before sending."
    if a.startswith("0x") and len(a) == 42:
        return "warn", f"{a} — EVM-format address. If not from a verified exchange, it may be a personal wallet."
    if a.startswith("bc1"):
        return "warn", f"{a} — BTC address. Verify the recipient before transferring funds."
    if len(a) < 15:
        return "bad", f"{a} — Invalid or too short address format."
    return "ok", f"{a} — No known risks detected (demo)."

@app.route("/", methods=["GET", "POST"])
def home():
    message = None
    css_class = ""
    addr = None

    if request.method == "POST":
        addr = request.form.get("address", "").strip()

        if addr in SCAM_ADDRESSES:
            reason = SCAM_ADDRESSES[addr]
            message = f"{addr} — ❌ Detected scam / fraudulent address! Reason: {reason}"
            css_class = "res-bad"
        elif addr in EXCHANGE_ADDRESSES:
            exch = EXCHANGE_ADDRESSES[addr]
            message = f"{addr} — ✅ Verified exchange / service address: {exch}."
            css_class = "res-ok"
        else:
            level, text = basic_heuristic(addr)
            message = text
            css_class = {
                "bad": "res-bad",
                "warn": "res-warn",
                "ok": "res-ok",
            }.get(level, "res-warn")

    return render_template_string(PAGE, message=message, css_class=css_class, addr=addr)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
