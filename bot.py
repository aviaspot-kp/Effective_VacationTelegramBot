import telebot
import threading
from utils import config
from utils.process_message import process
from flask import Flask, request

bot = telebot.TeleBot(config.TOKEN, threaded=False)
webhook = 'https://frozen-peak-06617.herokuapp.com/' + config.SECRET
#
if webhook != bot.get_webhook_info().url:
    bot.set_webhook(webhook)

app = Flask(__name__)


@app.route(f'/{config.SECRET}', methods=['POST'])
def webhook():
    message = request.get_json()
    if threading.active_count() < 10:
        threading.Thread(
            target=process,
            args=(message,)
        ).start()
    else:
        bot.send_message(
            message['message']['chat']['id'],
            'Сервис загружен, попробуйте позже...')
    return 'ok'


if __name__ == "__main__":
    app.run(debug=False)
