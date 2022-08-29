import flask
import os
import TGapi
import ShipFinder
app = flask.Flask(__name__)

@app.route("/", methods=['POST'])
def index():
    chat_id, user_name = TGapi.WH_analyse(flask.request.json)
    #msg = ShipFinder.main()
    msg = 'hi'
    TGapi.sendMsg(msg, chat_id, user_name)
    return 'hi'

if __name__ == '__main__':
    TGapi.deleteWH()
    TGapi.setWH('https://fortesty.herokuapp.com/')
    print('ready')
    app.run(host="https://fortesty.herokuapp.com/", port=int(os.environ.get("PORT", 8443)))
