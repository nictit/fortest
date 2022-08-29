import flask
import os
import TGapi
import ShipFinder
app = flask.Flask(__name__)

@app.route("/", methods=['POST'])
def index():
    chat_id, user_name = TGapi.WH_analyse(flask.request.json)
    msg = ShipFinder.main()
    print(msg)
    TGapi.sendMsg(msg, chat_id, user_name)
    return 'hi'

if __name__ == '__main__':
    TGapi.deleteWH()
    print('setting WH')
    TGapi.setWH('https://fortesty.herokuapp.com')
    print('WH set')
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
