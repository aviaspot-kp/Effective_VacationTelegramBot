import telebot
from utils import config
from utils.process_image import process_image
from utils.check_date import check_date

bot = telebot.TeleBot(config.TOKEN, threaded=False)


def invalid_command(message):
    bot.send_message(
        message['message']['chat']['id'],
        'Введите команду в формате:'
        '\n"В отпуске до ДД.ММ"')


def process(message):
    try:
        user_input = message['message']['text'].lower().split()
    except KeyError:
        invalid_command(message)
        return

    if ' '.join(user_input[0:3]) != 'в отпуске до':
        invalid_command(message)
        return

    try:
        if check_date(user_input[3]) != 'error':
            date, year = check_date(user_input[3])
        else:
            bot.send_message(
                message['message']['chat']['id'],
                'Дата введена неверно, попробуйте еще...')
            return
    except IndexError:
        invalid_command(message)
        return

    bot.send_message(
        message['message']['chat']['id'],
        f'Вы в отпуске до {date}.{year}'
        f'\nПодготовка аватарки, подождите...')

    user_id = message['message']['from']['id']
    try:
        file_id = bot.get_user_profile_photos(
            user_id=user_id,
            offset=0,
            limit=1).photos[0][2].file_id
    except IndexError:
        bot.send_message(
            message['message']['chat']['id'],
            'Не удалось получить Вашу аватарку...\n'
            'Пожалуйста, проверьте настройки конфиденциальности')
        return
    file_path = bot.get_file(file_id).file_path
    avatar = bot.download_file(file_path)

    bot.send_photo(
        message['message']['chat']['id'],
        photo=process_image(avatar, date))
