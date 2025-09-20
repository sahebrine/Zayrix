import re
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)
import requests
def fetch_users_from_text():
    data = {
    "articleId" : 76726741,
    "secureCode" : "g2tbrt1q9wfsga7f"
    }
    url = "https://justpaste.it/api/v1/existing-article"

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
        'Cookie': 'userData=WGkQkiQGty9YbFgNvvmOu2Q27FIBhb7LOYJYHHW6iPR-LImkRryVYavHk73ItZL6Pj7GsGDqMCjmYsIn9ITwye3lnXC1G9bfXYDxR-jxZN9bmzUThlbVZIx986pggRNdxvFowsDrf0iJRdysMQTUQhXGgrdUP2cSWSPmXWcybeUIgK_l6LLDqS82ufqj6G_tlW--C35lTA%3D%3D; user=34963e2fea5ea2f025c7f8e449f917000053b2bac2bd66eb8b2b9b7aafdebe6f96ba74a001e46228d50be0f709fa513766; PHPSESSID=1f6a70f44e296384222ab4f43bef6ff9',
        'Origin': 'https://justpaste.it',
        'Priority': 'u=1, i',
        'Referer': f'https://justpaste.it/edit/76726741/g2tbrt1q9wfsga7f',
        'Sec-CH-UA': '"Chromium";v="140", "Not=A?Brand";v="24", "Microsoft Edge";v="140"',
        'Sec-CH-UA-Arch': 'x86',
        'Sec-CH-UA-Bitness': '64',
        'Sec-CH-UA-Form-Factors': 'Desktop',
        'Sec-CH-UA-Full-Version-List': '"Chromium";v="140.0.7339.133", "Not=A?Brand";v="24.0.0.0", "Microsoft Edge";v="140.0.3485.66"',
        'Sec-CH-UA-Mobile': '?0',
        'Sec-CH-UA-Model': '',
        'Sec-CH-UA-Platform': '"Windows"',
        'Sec-CH-UA-Platform-Version': '10.0.0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0'
    }
    articleContent = requests.post(url, json=data, headers=headers)
    articleContent = str(articleContent.json()['articleContent']).replace("\\n", "\n")
    pattern = r"[🏆🥈🥉🎖#]\s*:\s*(.*?)\s*—\s*(\d+)\s*POINTS"
    matches = re.findall(pattern, articleContent)

    users = []
    for name, score in matches:
        users.append({"name": name.strip(), "score": int(score)})
    time_match = re.search(r"⏳ Time remaining this month:\s*(.*)", articleContent)
    time_remaining = time_match.group(1).strip() if time_match else "N/A"

    return users, time_remaining
@app.route("/")
def index():
    users, time_remaining = fetch_users_from_text()
    rows_html = ""
    medals = ["🏆", "🥈", "🥉", "🎖"]
    for i, u in enumerate(users, start=1):
        medal = medals[i-1] if i <= len(medals) else f"#{i}"
        rows_html += f"""
        <tr>
            <td>{medal}</td>
            <td>{u['name']}</td>
            <td>{u['score']}</td>
        </tr>
        """
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Zayrix Leaderboard</title>
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
    background: linear-gradient(270deg, #0d0d0d, #1a1a1a, #0d0d0d);
    background-size: 400% 400%;
    animation: blackGradient 8s ease infinite;
    border-bottom: 2px solid #ffffff33;
    box-shadow: 0 0 15px rgba(255,255,255,0.1);
}}

    .username, .info {{
        font-size: 18px;
        margin: 5px 0;
        font-weight: 700;
        background: linear-gradient(270deg, #fffefe, #cacaca, #858585);
        background-size: 600% 600%;
        animation: textGradient 2s linear infinite;
        -webkit-background-clip: text;
        color: transparent;
    }}
    .avatar {{
        width: 120px; height: 120px;
        border-radius: 100%;
    }}
    .username {{ font-size: 28px; margin-top: 10px; }}

.header h1 {{
    font-size: 26px;
    margin: 10px 0;
    background: linear-gradient(270deg, #fffefe, #cacaca, #858585);
    background-size: 600% 600%;
    animation: textGradient 3s linear infinite;
    -webkit-background-clip: text;
}}

.leaderboard {{
    margin: 30px auto;
    width: 90%;
    max-width: 600px;
    border-collapse: collapse;
    background: #111;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 0 10px rgba(255,255,255,0.3);
    animation: fadeIn 1.5s ease-in-out;
}}

.leaderboard th, .leaderboard td {{
    padding: 15px;
    text-align: center;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}}

.leaderboard th {{
    background: #1a1a1a;
    font-size: 16px;
    font-weight: 700;
}}

.leaderboard tr:nth-child(odd) {{
    background: rgba(255,255,255,0.03);
}}

.leaderboard tr:hover {{
    background: rgba(255,255,255,0.1);
}}

.time-remaining {{
    margin-top: 15px;
    font-size: 14px;
    color: #ccc;
}}

.footer {{
    margin: 20px 10px;
    font-size: 14px;
    color: rgba(255,255,255,0.5);
}}

@keyframes textGradient {{
    0% {{background-position: 0% 50%;}}
    50% {{background-position: 100% 50%;}}
    100% {{background-position: 0% 50%;}}
}}

@keyframes fadeIn {{
    from {{opacity:0; transform: translateY(20px);}}
    to {{opacity:1; transform: translateY(0);}}
}}
</style>
</head>
<body>
<div class="header">
    <img src="https://cdn.discordapp.com/attachments/1370733349995548682/1418747942466093188/6E5EC9B7-5174-4B00-8FD2-6E73E5FB946D.png?ex=68cf3f7c&is=68cdedfc&hm=4e4f870113962efdbd93774d6faa00fcff1c7aaea3b119be1a38bbeed4bc66a4&" class="avatar">
    <div class="username">Zayrix Top Leaderboard</div>
    <div class="info">Time: {datetime.now().strftime('%Y/%m/%d %I:%M:%S %p')}</div>
</div>

<table class="leaderboard">
    <tr>
        <th>Rank</th>
        <th>User</th>
        <th>Points</th>
    </tr>
    {rows_html}
</table>

<div class="time-remaining">⏳ Time remaining this month: {time_remaining}</div>

<div class="footer">Zayrix Swapper - Developed by @sahe</div>
</body>
</html>
"""
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
