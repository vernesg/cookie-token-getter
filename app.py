from flask import Flask, render_template, request
import requests, re

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    token_result = ""
    if request.method == "POST":
        cookie = request.form.get("cookie", "")
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.86 Mobile Safari/537.36',
                'referer': 'https://m.facebook.com/',
                'host': 'm.facebook.com',
                'origin': 'https://m.facebook.com',
                'upgrade-insecure-requests': '1',
                'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
                'cache-control': 'max-age=0',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'content-type': 'text/html; charset=utf-8'
            }

            cookies = {'cookie': cookie}

            res = requests.get('https://m.facebook.com/composer/ocelot/async_loader/?publisher=feed#_=_', headers=headers, cookies=cookies)
            token_match = re.search(r'(EAAA\w+)', res.text)

            if token_match:
                token_result = f"✅ Access Token:\n{token_match.group(1)}"
            else:
                token_result = "❌ Fail: Maybe your cookie is invalid!"
        except requests.exceptions.ConnectionError:
            token_result = "❌ Fail: No connection!"
        except Exception as e:
            token_result = f"❌ Fail: Unknown error - {str(e)}"

    return render_template("index.html", result=token_result)