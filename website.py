from flask import Flask, render_template_string, request
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    username = request.args.get("username", "guest")
    expiry = request.args.get("expiry", "∞ days left")
    stats = {}
    sections = ["swap", "bypass", "claim"]
    for sec in sections:
        stats[sec] = {
            "TOTAL": int(request.args.get(f"{sec}_TOTAL", 0)),
            "2L": int(request.args.get(f"{sec}_2L", 0)),
            "3L": int(request.args.get(f"{sec}_3L", 0)),
            "4L": int(request.args.get(f"{sec}_4L", 0)),
            "DOUBLES": int(request.args.get(f"{sec}_DOUBLES", 0)),
            "TRIPLES": int(request.args.get(f"{sec}_TRIPLES", 0)),
            "OTHERS": int(request.args.get(f"{sec}_OTHERS", 0)),
        }
    selected_section = None
    if request.method == "POST":
        if "btn1" in request.form:
            selected_section = "swap"
        elif "btn2" in request.form:
            selected_section = "bypass"
        elif "btn3" in request.form:
            selected_section = "claim"
        elif "back" in request.form:
            selected_section = None
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
    margin: 0;
    padding: 0;
    font-family: 'Poppins', sans-serif;
    text-align: center;
    color: #fff;
    background: linear-gradient(270deg, #000000, #111111, #1c1c1c, #000000);
    background-size: 600% 600%;
    animation: blackGradient 10s ease infinite;
}


    @keyframes bgGradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    .header {
    padding: 20px;
    background: linear-gradient(270deg, #0d0d0d, #1a1a1a, #0d0d0d);
    background-size: 400% 400%;
    animation: blackGradient 8s ease infinite;
    border-bottom: 2px solid #ffffff33;
    box-shadow: 0 0 15px rgba(255,255,255,0.1);
}

    .username, .info {
        font-size: 18px;
        margin: 5px 0;
        font-weight: 700;
        background: linear-gradient(270deg, #fffefe, #cacaca, #858585);
        background-size: 600% 600%;
        animation: textGradient 2s linear infinite;
        -webkit-background-clip: text;
        color: transparent;
    }
    .avatar {
        width: 80px; height: 80px;
        border-radius: 100%;
    }
    .username { font-size: 28px; margin-top: 10px; }

    .buttons {
        margin: 30px auto;
        display: flex;
        flex-direction: column;
        gap: 15px; 
        align-items: center;
        width: fit-content;
    }
    .btn {
    padding: 15px 30px;
    font-size: 18px;
    font-weight: 600;
    color: white;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    background: linear-gradient(270deg, #000000, #141414, #1f1f1f, #000000);
    background-size: 600% 600%;
    animation: blackGradient 4s linear infinite;
    box-shadow: 0 0 8px rgba(255,255,255,0.1);
    transition: transform 0.2s ease-in-out, box-shadow 0.2s;
}
    .btn:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px rgba(255,255,255,0.3);
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
        box-shadow: 0 0 8px #ffffff;
    }
   .card-inner {
    width: 100%; height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center; 
    align-items: center;
    background: linear-gradient(270deg, #000000, #1a1a1a, #2b2b2b, #000000);
    background-size: 600% 600%;
    animation: blackGradient 6s ease infinite;
    color: #fff; 
    font-weight: 600;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
}

@keyframes blackGradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
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
        color: rgba(255,255,255,0.8);
    }
    </style>
    </head>
    <body>
    <div class="header">
        <img src="https://cdn.discordapp.com/attachments/1370733349995548682/1418747942466093188/6E5EC9B7-5174-4B00-8FD2-6E73E5FB946D.png?ex=68cf3f7c&is=68cdedfc&hm=4e4f870113962efdbd93774d6faa00fcff1c7aaea3b119be1a38bbeed4bc66a4&" class="avatar">
        <div class="username">{{ username }}</div>
        <div class="info">Expiry: {{ expiry }}</div>
        <div class="info">Time: {{ now }}</div>
    </div>

    <form method="post">
        {% if not section %}
        <div class="buttons">
            <button class="btn" type="submit" name="btn1">Swap Statistics</button>
            <button class="btn" type="submit" name="btn2">Bypass Statistics</button>
            <button class="btn" type="submit" name="btn3">Claim Statistics</button>
        </div>
        {% else %}
        <div class="section">
            <div class="cards">
            {% for key, value in stats[section].items() %}
                <div class="card"><div class="card-inner">
                    <h3>{{ key }}</h3>
                    <p>{{ value }}</p>
                </div></div>
            {% endfor %}
            </div>
        </div>
        <div class="buttons">
            <button class="btn" type="submit" name="back"> Back</button>
        </div>
        {% endif %}
    </form>

    <div class="footer">Zayrix Swapper - Developed by @sahe</div>
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
    app.run(host="0.0.0.0", port=5000)















