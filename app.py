from flask import Flask, request, render_template_string

app = Flask(__name__)

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
            max-width: 600px;
            width: 100%;
            padding: 25px 30px 30px;
            border-radius: 14px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        }
        h1 {
            margin-top: 0;
            font-size: 26px;
        }
        p.subtitle {
            color: #555;
            margin-top: 4px;
            margin-bottom: 20px;
        }
        form input[type=text] {
            width: 100%;
            padding: 12px;
            font-size: 15px;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            outline: none;
        }
        form button {
            margin-top: 14px;
            background: #4f46e5;
            color: #fff;
            border: none;
            padding: 10px 18px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
        }
        form button:hover {
            background: #4338ca;
        }
        .result {
            margin-top: 20px;
            padding: 14px 14px 14px 38px;
            border-radius: 10px;
            background: #fef3c7;
            border: 1px solid #fbbf24;
            position: relative;
        }
        .result::before {
            content: "⚠";
            position: absolute;
            left: 12px;
            top: 12px;
        }
        .ok {
            background: #dcfce7;
            border: 1px solid #22c55e;
        }
        .ok::before {
            content: "✅";
        }
        .small {
            margin-top: 18px;
            font-size: 12px;
            color: #6b7280;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>🔐 Personal Wallet Warning Signal</h1>
        <p class="subtitle">
            Kripto jo‘natishdan oldin manzilni tekshiring. Shubhali / shaxsiy (EOA) bo‘lsa — ogohlantiramiz.
        </p>
        <form method="POST">
            <label>Wallet manzilini kiriting:</label><br>
            <input type="text" name="address" placeholder="0x..., T..., bc1..." required value="{{ addr or '' }}">
            <button type="submit">Tekshirish</button>
        </form>

        {% if message %}
            <div class="result {% if safe %}ok{% endif %}">
                {{ message }}
            </div>
        {% endif %}

        <p class="small">
            Demo versiya. Haqiqiy tahlil: zanjirga, birja ro‘yxatiga, qora ro‘yxatga va bot faoliyatiga ulanadi.
        </p>
    </div>
</body>
</html>
"""

def check_address(addr: str):
    """
    Juda sodda, demo tekshiruv.
    Keyinchalik bu yerga:
     - birja manzillari ro‘yxati
     - block explorer API
     - scam list
    qo‘shamiz.
    """
    if not addr:
        return False, "Manzil bo‘sh."
    a = addr.strip()

    # TRON
    if a.startswith("T") and len(a) > 20:
        return False, f"{a} — TRON tarmog‘ida ehtimoliy shaxsiy hamyon (EOA). Jo‘natishda ikki marta tekshiring."
    # EVM (ETH, BNB, Polygon)
    if a.startswith("0x") and len(a) == 42:
        return False, f"{a} — EVM formatidagi manzil. Agar bu birja manzili bo‘lmasa, foydalanuvchi hamyoni bo‘lishi mumkin."
    # BTC bech32
    if a.startswith("bc1"):
        return False, f"{a} — BTC bech32 manzili. Qabul qiluvchi kimligini tasdiqlang."
    # Juda qisqa yoki g‘alati
    if len(a) < 15:
        return False, f"{a} — manzil juda qisqa yoki noto‘g‘ri ko‘rinadi."

    return True, f"{a} — hozircha xavf aniqlanmadi (demo)."

@app.route("/", methods=["GET", "POST"])
def home():
    message = None
    safe = False
    addr = None
    if request.method == "POST":
        addr = request.form.get("address")
        safe, message = check_address(addr)
    return render_template_string(PAGE, message=message, safe=safe, addr=addr)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
