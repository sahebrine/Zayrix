from flask import Flask, render_template_string, request
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    username = request.args.get("username", "guest")
    expiry = request.args.get("expiry", "∞ days left")

    # استخراج الإحصائيات من الرابط
    stats = {}
    sections = ["swap", "bypass", "claim"]
    for sec in sections:
        stats[sec] = {
            "TOTAL": int(request.args.get(f"{sec}_TOTAL", 0)),
            "1L": int(request.args.get(f"{sec}_1L", 0)),
            "2L": int(request.args.get(f"{sec}_2L", 0)),
            "3L": int(request.args.get(f"{sec}_3L", 0)),
            "4L": int(request.args.get(f"{sec}_4L", 0)),
            "DOUBLES": int(request.args.get(f"{sec}_DOUBLES", 0)),
            "TRIPLES": int(request.args.get(f"{sec}_TRIPLES", 0)),
            "OTHERS": int(request.args.get(f"{sec}_OTHERS", 0)),
        }

    # تحديد القسم المطلوب بناءً على الزر
    selected_section = None
    if request.method == "POST":
        if "btn1" in request.form:
            selected_section = "swap"
        elif "btn2" in request.form:
            selected_section = "bypass"
        elif "btn3" in request.form:
            selected_section = "claim"

    # HTML الأساسي
    base_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zayrix Stats for {{ username }}</title>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    body {
        background: #0a0a0a;
        color: #fff;
        font-family: 'Poppins', sans-serif;
        margin: 0; padding: 0;
        text-align: center;
    }
    .header {
        padding: 20px;
        background: #111;
        border-bottom: 2px solid #ffffff;
        box-shadow: 0 0 15px rgba(255,255,255,0.5);
    }
    .header .username,
    .header .info {
        font-size: 18px;
        margin: 5px 0;
        font-weight: 700;
        background: linear-gradient(270deg, #fffefe, #cacaca, #858585);
        background-size: 600% 600%;
        animation: textGradient 2s linear infinite;
        -webkit-background-clip: text;
    }
    .avatar {
        width: 200px; height: 200px;
        border-radius: 50%;
    }
    .username { font-size: 28px; margin-top: 10px; }
    .info { font-size: 18px; margin: 5px 0; }

    .buttons {
        margin: 30px;
        display: flex;
        justify-content: center;
        gap: 20px;
    }
    .btn {
        padding: 15px 30px;
        font-size: 18px;
        font-weight: 600;
        color: white;
        background: linear-gradient(270deg, #1a1a1a, #333, #1a1a1a);
        border: 2px solid white;
        border-radius: 12px;
        cursor: pointer;
        transition: 0.3s;
    }
    .btn:hover {
        background: white;
        color: black;
    }

    .section { margin: 20px 10px; }
    .section h2 { font-size: 20px; margin-bottom: 15px; }
    .cards {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
    }
    .card {
        width: 120px; height: 120px;
        border-radius: 12px;
        overflow: hidden;
        position: relative;
        box-shadow: 0 0 5px #ffffff;
    }
    .card-inner {
        width: 100%; height: 100%;
        display: flex; flex-direction: column;
        justify-content: center; align-items: center;
        background: linear-gradient(270deg, #0f0f0f, #1a1a1a, #0f0f0f);
        background-size: 600% 600%;
        animation: innerGradient 2s linear infinite;
        color: #ffffff; font-weight: 600;
    }
    .card h3 { font-size: 14px; margin-bottom: 5px; }
    .card p { font-size: 20px; margin: 0; }

    @keyframes innerGradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    @keyframes textGradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .footer {
        margin: 20px 10px;
        font-size: 14px;
        color: rgba(255,255,255,0.5);
    }
    </style>
    </head>
    <body>
    <div class="header">
        <img src="https://cdn.discordapp.com/attachments/1370733349995548682/1418595688836632667/6E5EC9B7-5174-4B00-8FD2-6E73E5FB946D.png?ex=68ceb1b0&is=68cd6030&hm=a32685de1baa2460d1b7e009c40435a8de0ad63b3fa2738604414ed2460c29a1&" class="avatar">
        <div class="username">👤 {{ username }}</div>
        <div class="info">📆 Expiry: {{ expiry }}</div>
        <div class="info">🕔 Generated: {{ now }}</div>
    </div>

    <form method="post">
        <div class="buttons">
            <button class="btn" type="submit" name="btn1">Swap Statistics</button>
            <button class="btn" type="submit" name="btn2">Bypass Statistics</button>
            <button class="btn" type="submit" name="btn3">Claim Statistics</button>
        </div>
    </form>

    {% if section %}
    <div class="section">
        <h2>{{ section|capitalize }} Statistics</h2>
        <div class="cards">
        {% for key, value in stats[section].items() %}
            <div class="card"><div class="card-inner">
                <h3>{{ key }}</h3>
                <p>{{ value }}</p>
            </div></div>
        {% endfor %}
        </div>
    </div>
    {% endif %}

    <div class="footer">Zayrix Swapper - Developed by @cahe</div>
    </body>
    </html>
    """

    return render_template_string(
        base_template,
        username=username,
        expiry=expiry,
        now=datetime.now().strftime('%Y/%m/%d %I:%M:%S %p'),
        stats=stats,
        section=selected_section
    )


if __name__ == "__main__":
    app.run(debug=True)
