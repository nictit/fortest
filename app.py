import flask
import os
import requests
import add
import TGapi

app = flask.Flask(__name__)

@app.route("/", methods=['POST'])
def index():
    chat_id, user_name = TGapi.WH_analyse(flask.request.json)
    TGapi.sendMsg('working', chat_id, user_name)
    requests.post('https://api.telegram.org/bot5048232576:AAHKQXWuVI-KIFQOEsDEizTGo9A1Ahjk4cw/sendMessage?text=' + add.text + '&chat_id=659584153')
    return 'hi'

if __name__ == '__main__':
    TGapi.deleteWH()
    TGapi.setWH('https://testapppper.herokuapp.com/')
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 80)))