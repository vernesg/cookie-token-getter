from flask import Flask, render_template, request
import requests, re

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    token_result = ""
    if request.method == "POST":
        cookie = request.form.get("cookie")
        try:
            data = requests.get('https://m.facebook.com/composer/ocelot/async_loader/?publisher=feed#_=_', headers={
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.86 Mobile Safari/537.36',
                'referer': 'https://m.facebook.com/',
                'host': 'm.facebook.com',
                'origin': 'https://m.facebook.com',
                'upgrade-insecure-requests': '1',
                'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
                'cache-control': 'max-age=0',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'content-type': 'text/html; charset=utf-8'
            }, cookies={
                'cookie': cookie
            })
            find_token = re.search('(EAAA\w+)', data.text)
            if find_token:
                token_result = f"Your Facebook Access Token:<br><code>{find_token.group(1)}</code>"
            else:
                token_result = "❌ Failed: Invalid cookie or token not found."
        except requests.exceptions.ConnectionError:
            token_result = "❌ Failed: No internet connection."
        except:
            token_result = "❌ Failed: Unknown error occurred."
    return render_template("index.html", token=token_result)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)