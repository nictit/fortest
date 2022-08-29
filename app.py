import flask
import os
import TGapi
import ShipFinder
import statistic
app = flask.Flask(__name__)

@app.route("/", methods=['POST'])
def index():
    chat_id, user_name, msg_text = TGapi.WH_analyse(flask.request.json)
    if msg_text == 'Количество запросов':
        msg = statistic.jsonRead()
    else:
        msg = ShipFinder.main()
        statistic.counter()
    print(msg)
    TGapi.sendMsg(str(msg), chat_id, user_name)
    return 'hi'

if __name__ == '__main__':
    TGapi.deleteWH()
    print('setting WH')
    TGapi.setWH('https://fortesty.herokuapp.com')
    print('WH set')
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# bot.send_document(message.chat.id, open(r'Путь_к_документу/Название_документа.txt, 'rb'))