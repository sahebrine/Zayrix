from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    username = request.args.get("username", "guest")
    expiry = request.args.get("expiry", "∞ days left")
    
    # Swap statistics
    swap = {k: int(request.args.get(k, 0)) for k in ["TOTAL","1L","2L","3L","4L","DOUBLES","TRIPLES","OTHERS"]}
    bypass = {k: int(request.args.get(f"b_{k}", 0)) for k in ["TOTAL","1L","2L","3L","4L","DOUBLES","TRIPLES","OTHERS"]}
    claim = {k: int(request.args.get(f"c_{k}", 0)) for k in ["TOTAL","1L","2L","3L","4L","DOUBLES","TRIPLES","OTHERS"]}

    sections = {
        "Swap Statistics": swap,
        "Bypass Statistics": bypass,
        "Claim Statistics": claim
    }

    sections_names = ["swap", "bypass", "claim"]
    sections = {}

    for sec in sections_names:
        sections[sec.capitalize() + " Statistics"] = {
            "TOTAL": request.args.get(f"{sec}_TOTAL", 0),
            "1L": request.args.get(f"{sec}_1L", 0),
            "2L": request.args.get(f"{sec}_2L", 0),
            "3L": request.args.get(f"{sec}_3L", 0),
            "4L": request.args.get(f"{sec}_4L", 0),
            "DOUBLES": request.args.get(f"{sec}_DOUBLES", 0),
            "TRIPLES": request.args.get(f"{sec}_TRIPLES", 0),
            "OTHERS": request.args.get(f"{sec}_OTHERS", 0)
        }

    # توليد HTML
    sections_html = ""
    for section_name, stats in sections.items():
        sections_html += f'<div class="section"><h2 style="color:#ffffff">{section_name}</h2><div class="cards">'
        for key, value in stats.items():
            sections_html += f'<div class="card"><div class="card-inner"><h3>{key}</h3><p>{value}</p></div></div>'
        sections_html += "</div></div>"

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Zayrix Stats for {username}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

body {{
    background: #0a0a0a;
    color: #fff;
    font-family: 'Poppins', sans-serif;
    margin: 0; padding: 0;
    text-align: center;
}}

.header {{
    padding: 20px;
    background: #111;
    border-bottom: 2px solid #ffffff;
    box-shadow: 0 0 15px rgba(255,255,255,0.5);
}}

.header .username,
.header .info {{
    font-size: 18px;
    margin: 5px 0;
    font-weight: 700;
    background: linear-gradient(270deg, #fffefe, #cacaca, #858585);
    background-size: 600% 600%;
    animation: textGradient 2s linear infinite;
    -webkit-background-clip: text;
}}

.avatar {{
    width: 200px; height: 200px;
    border-radius: 50%;
}}
.username {{
    font-size: 28px;
    margin-top: 10px;
}}
.info {{
    font-size: 18px;
    margin: 5px 0;
}}

.section {{
    margin: 20px 10px;
}}
.section h2 {{
    font-size: 20px;
    margin-bottom: 15px;
}}

.cards {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px;
}}

.card {{
    width: 120px;
    height: 120px;
    border-radius: 12px;
    overflow: hidden;
    position: relative;
    box-shadow: 0 0 5px #ffffff;
}}

.card-inner {{
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: linear-gradient(270deg, #0f0f0f, #1a1a1a, #0f0f0f);
    background-size: 600% 600%;
    animation: innerGradient 2s linear infinite;
    color: #ffffff;
    font-weight: 600;
}}

.card h3 {{ font-size: 14px; margin-bottom: 5px; }}
.card p {{ font-size: 20px; margin: 0; }}

@keyframes innerGradient {{
    0% {{background-position: 0% 50%;}}
    50% {{background-position: 100% 50%;}}
    100% {{background-position: 0% 50%;}}
}}

@keyframes textGradient {{
    0% {{background-position: 0% 50%;}}
    50% {{background-position: 100% 50%;}}
    100% {{background-position: 0% 50%;}}
}}

.footer {{
    margin: 20px 10px;
    font-size: 14px;
    color: rgba(255,255,255,0.5);
}}

@media (max-width: 600px) {{
    .card {{ width: 45%; height: 100px; }}
    .username {{ font-size: 20px; }}
    .info {{ font-size: 14px; }}
}}
</style>
</head>
<body>
<div class="header">
    <img src="https://cdn.discordapp.com/attachments/1370733349995548682/1418595688836632667/6E5EC9B7-5174-4B00-8FD2-6E73E5FB946D.png?ex=68ceb1b0&is=68cd6030&hm=a32685de1baa2460d1b7e009c40435a8de0ad63b3fa2738604414ed2460c29a1&" class="avatar">
    <div class="username">👤 {username}</div>
    <div class="info">📆 Expiry: {expiry}</div>
    <div class="info">🕔 Generated: {datetime.now().strftime('%Y/%m/%d %I:%M:%S %p')}</div>
</div>
{sections_html}
<div class="footer">Zayrix Swapper - Developed by @cahe</div>
</body>
</html>
"""
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
