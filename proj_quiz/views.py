from . import quiz
from django.conf import settings
import telebot
from telebot import types


TOKEN = settings.TELEGRAM_API_TOKEN
bot = telebot.TeleBot(TOKEN)


"""Глобальная переменная, в которой хранится словарь:
ключи -- ключи сессий, значения -- объекты Quiz."""
global quizzes


def check_answer(message):
    if 'quizzes' in globals() and quizzes[message.from_user.id].is_start:
        quiz.write_rus_name(quizzes[message.from_user.id].name, message.text)
        quizzes[message.from_user.id].is_start = False

    else:
        bot.send_message(message.from_user.id, '<b>Here is my feature list:</b>\n\n'
                                          '- Enter a <b>brand name</b> to see if '
                                               'it is continuing business in Russia'
                                          '\n\n'
                                          '- Enter a <b>country name</b> to see all its working brands'
                                          '\n\n'
                                          '- If you want see the list of rebranded companies type <b>rebranded</b>',
                         parse_mode='html')
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        item1 = types.InlineKeyboardButton('Choose country')
        item2 = types.InlineKeyboardButton('rebranded')
        markup.add(item1, item2)

        bot.send_message(message.from_user.id, text='Choose action:', reply_markup=markup)


def start(message):
    global quizzes
    if 'quizzes' in globals():
        quizzes[message.from_user.id] = quiz.Quiz(message.text)
    else:
        quizzes = dict()
        quizzes[message.from_user.id] = quiz.Quiz(message.text)


@bot.message_handler(content_types=['text'])
def message_reply(message):
    if quiz.country_check(message.text):
        info = quiz.get_info(country_info=message.text)
        bot.send_message(message.from_user.id, f'Brands from {message.text} operating in Russia:\n\n'+''
                         .join([f'{x}\n' for x in info]))
    elif quiz.name_check(message.text):
        info = quiz.get_info(name_info=message.text)
        start(message)
        bot.send_message(message.from_user.id, f'Name: {info[0]}\n\n'
                                               f'Action: {info[1]}\n\n'
                                               f'Industry: {info[2]}\n\n'
                                               f'Country: {info[3]}\n\n'+''
                         .join([f'Текущее имя: {info[4]}\n\n' if len(info) == 5 else '']))
        bot.send_message(message.from_user.id, f'If you know how this brand is currently called in Russia, then please '
                                               f'write \'имя\'')
    elif message.text == 'имя':
        quizzes[message.from_user.id].is_start = True
        bot.send_message(message.from_user.id, 'Write the name of the brand in Russia')
    elif message.text == 'rebranded':
        bot.send_message(message.from_user.id, quiz.rebranded())
    elif message.text == 'Choose country':
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        for country in quiz.get_countries():
            markup.add(types.InlineKeyboardButton(country))
        bot.send_message(message.from_user.id, text='List of countries:', reply_markup=markup)
    else:
        check_answer(message)


bot.polling(non_stop=True)
