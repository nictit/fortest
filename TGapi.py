import requests

#https://api.telegram.org/bot5048232576:AAHKQXWuVI-KIFQOEsDEizTGo9A1Ahjk4cw/getUpdates
api_url = 'https://api.telegram.org/bot'
token = '5048232576:AAHKQXWuVI-KIFQOEsDEizTGo9A1Ahjk4cw'
url = api_url + token + '/'

# for testing
def getUpdate():
    update_response = requests.post('https://api.telegram.org/bot5048232576:AAHKQXWuVI-KIFQOEsDEizTGo9A1Ahjk4cw/getUpdates').json()
    return update_response


# set up webhook with given url
# return true if all is ok
def setWH(WH_url):
    json1 = {"url": WH_url}
    setWH_response = requests.post(url + 'setWebhook', json1)
    return setWH_response.json()['ok']

def deleteWH():
    deleteWH_response = requests.post(url + 'deleteWebhook')
    return deleteWH_response.json()['ok']


# return chat_id (to response the user) and user's name
#  who triggered webhook with ANY action
# !!! change "[-1]" before setting webhook up !!!
def WH_analyse(WH_triggered):
    chat_id = WH_triggered['message']['from']['id']
    user_name = WH_triggered['message']['from']['first_name']
    msg_text = WH_triggered['message']['text']
    return chat_id, user_name, msg_text

# send message to user, who triggered webhook
# return true if all is ok
def sendMsg(ships_text, chat_id, user_name):
    msgText = 'Привет, ' + '*' + user_name + '*'  + '\n' + '`' + ships_text + '`'
    msgJson = {
        "text": msgText,
        "chat_id": chat_id,
        "parse_mode": "Markdown"
              }
    sendMsg_response = requests.post('https://api.telegram.org/bot5048232576:AAHKQXWuVI-KIFQOEsDEizTGo9A1Ahjk4cw/sendMessage', msgJson)
    return sendMsg_response.json()['ok']
