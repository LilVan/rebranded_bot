import copy
from django.shortcuts import render, redirect
from django.core.cache import cache
from . import terms_work
from . import quiz
from django.conf import settings
import telebot

TOKEN = settings.TELEGRAM_API_TOKEN
bot = telebot.TeleBot(TOKEN)


def index(request):
    return render(request, "index.html")


def terms_list(request):
    terms = terms_work.get_terms_for_table()
    return render(request, "term_list.html", context={"terms": terms})


def add_term(request):
    return render(request, "term_add.html")


def send_term(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        new_term = request.POST.get("new_term", "")
        new_definition = request.POST.get("new_definition", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_definition) == 0:
            context["success"] = False
            context["comment"] = "Описание должно быть не пустым"
        elif len(new_term) == 0:
            context["success"] = False
            context["comment"] = "Термин должен быть не пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваш термин принят"
            terms_work.write_term(new_term, new_definition)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "term_request.html", context)
    else:
        add_term(request)


def show_stats(request):
    stats = terms_work.get_terms_stats()
    return render(request, "stats.html", stats)


"""Глобальная переменная, в которой хранится словарь:
ключи -- ключи сессий, значения -- объекты Quiz."""
global quizzes

"""
def start_quiz(request):
    if not request.session.session_key:
        request.session.create()

    global quizzes
    if 'quizzes' in globals():
        quizzes[request.session.session_key] = quiz.Quiz()
    else:
        quizzes = dict()
        quizzes[request.session.session_key] = quiz.Quiz()

    return render(request, "quiz.html", context={"terms": quizzes[request.session.session_key].qna,
                                                 "quiz_start": True})
"""


def check_quiz(request):
    if request.method == "POST":
        global quizzes
        for i in range(1, 5+1):  # TODO: вынести количество вопросов в .env
            quizzes[request.session.session_key]\
                .record_user_answer(request.POST.get("answer" + "-" + str(i)))
        terms = copy.copy(quizzes[request.session.session_key].qna)
        answers = copy.copy(quizzes[request.session.session_key].get_user_answers())
        marks = copy.copy(quizzes[request.session.session_key].check_quiz())
        del quizzes[request.session.session_key]
        return render(request, "quiz.html", context={"terms": terms,
                                                     "quiz_start": False,
                                                     "answers": answers,
                                                     "marks": marks})
    return redirect("/quiz")


def check_answer(name, message):
    if 'quizzes' in globals() and quizzes[message.from_user.id].is_start:
        quiz.write_rus_name(name, message.text)
        quizzes[message.from_user.id].is_start = False

    else:
        bot.send_message(message.chat.id, 'Please enter a brand name to see if it is continuing business in Russia'
                                          '\n\n'
                                          'Enter a country name to see all its working brands'
                                          '\n\n'
                                          'If you want to add a business operating in Russia print \'add\'')


def start(message):
    global quizzes
    if 'quizzes' in globals():
        quizzes[message.from_user.id] = quiz.Quiz(message.text)
    else:
        quizzes = dict()
        quizzes[message.from_user.id] = quiz.Quiz(message.text)

    # term = quizzes[message.from_user.id].next_qna()[1]


@bot.message_handler(content_types=['text'])
def message_reply(message):
    if quiz.country_check(message.text):
        info = quiz.get_info(country_info=message.text)
        bot.send_message(message.chat.id, f'Brands from {message.text} operating in Russia:\n\n'+''
                         .join([f'{x}\n' for x in info]))
    elif quiz.name_check(message.text):
        info = quiz.get_info(name_info=message.text)
        start(message)
        bot.send_message(message.chat.id, f'Name: {info[0]}\n\n'
                                          f'Action: {info[1]}\n\n'
                                          f'Industry: {info[2]}\n\n'
                                          f'Country: {info[3]}\n\n'+''
                         .join([f'Текущее имя: {info[4]}\n\n' if len(info) == 5 else '']))
        bot.send_message(message.chat.id, f'If you know how this brand is currently called in Russia, then please '
                                          f'write \'имя\'')
    elif message.text == 'имя':
        bot.send_message(message.chat.id, 'Write the name of the brand in Russian')
    else:
        check_answer(quizzes[message.from_user.id].name, message)


bot.polling(non_stop=True)
