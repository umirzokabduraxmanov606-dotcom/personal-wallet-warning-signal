from flask import Flask, request, render_template_string

app = Flask(__name__)

# 1) Birja / xavfsiz manzillar (demo)
EXCHANGE_ADDRESSES = {
    # bu yerga haqiqiy manzillarni ham qo‘shib borasan
    "0x1111111111111111111111111111111111111111": "Demo CEX (Ethereum)",
    "TXXXXEXCHANGEADDRESSDEMO111": "Demo TRON Exchange",
}

# 2) Scam / shubhali manzillar (demo)
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
            Manzilni kiriting — tizim uni ma'lum scam ro‘yxati, birja manzillari va oddiy nazorat qoidalari bo‘yicha tekshiradi.
        </p>
        <form method="POST">
            <label>Wallet manzili:</label><br>
            <input type="text" name="address" placeholder="0x..., T..., bc1..." required value="{{ addr or '' }}">
            <button type="submit">Tekshirish</button>
        </form>

        {% if message %}
            <div class="result {{ css_class }}">
                {{ message }}
            </div>
        {% endif %}

        <p class="small">
            Demo versiya. Siz bu ro‘yxatlarni API yoki ma'lumotlar bazasidan avtomatik yangilanishi uchun ulashingiz mumkin.
            <br>
            <b>Owner:</b> Umirzok Mamatmurodovich Abduraxmanov <span class="tag">PWWS</span>
        </p>
    </div>
</body>
</html>
"""

def basic_heuristic(a: str):
    # Hech narsaga tushmasa — eski tekshiruv
    if a.startswith("T") and len(a) > 20:
        return "warn", f"{a} — TRON tarmog‘ida ehtimoliy shaxsiy hamyon (EOA). Jo‘natishdan oldin tasdiqlang."
    if a.startswith("0x") and len(a) == 42:
        return "warn", f"{a} — EVM formatidagi manzil. Agar birja manzili bo‘lmasa, bu shaxsiy hamyon bo‘lishi mumkin."
    if a.startswith("bc1"):
        return "warn", f"{a} — BTC manzili. Qabul qiluvchi shaxsni tasdiqlang."
    if len(a) < 15:
        return "bad", f"{a} — manzil juda qisqa yoki noto‘g‘ri ko‘rinadi."
    return "ok", f"{a} — ma'lum xavf topilmadi (demo)."

@app.route("/", methods=["GET", "POST"])
def home():
    message = None
    css_class = ""
    addr = None

    if request.method == "POST":
        addr = request.form.get("address", "").strip()

        # 1) SCAM ro‘yxati bo‘yicha
        if addr in SCAM_ADDRESSES:
            reason = SCAM_ADDRESSES[addr]
            message = f"{addr} — ❌ SCAM / firibgarlik bilan bog‘liq manzil! Sabab: {reason}"
            css_class = "res-bad"
        # 2) Exchange / xavfsiz ro‘yxati bo‘yicha
        elif addr in EXCHANGE_ADDRESSES:
            exch = EXCHANGE_ADDRESSES[addr]
            message = f"{addr} — ✅ tanilgan exchange / xizmat manzili: {exch}."
            css_class = "res-ok"
        else:
            # 3) Hech qaysiga tushmasa — evristik
            level, text = basic_heuristic(addr)
            message = text
            css_class = {
                "bad": "res-bad",
                "warn": "res-warn",
                "ok": "res-ok",
            }.get(level, "res-warn")

    return render_template_string(PAGE, message=message, css_class=css_class, addr=addr)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
