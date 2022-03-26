import flask
import os
import requests
import add

app = flask.Flask(__name__)

@app.route("/")
def index():
    text = flask.request.json['a']
    requests.post('https://api.telegram.org/bot5048232576:AAHKQXWuVI-KIFQOEsDEizTGo9A1Ahjk4cw/sendMessage?text=' + add.text + '&chat_id=659584153')
    return 'hi'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8443)))