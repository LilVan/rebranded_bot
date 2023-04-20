from django.shortcuts import render, redirect
from django.core.cache import cache
from . import terms_work
from . import quiz
import django.contrib.messages


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


def check_quiz(request):
    if request.method == "POST":
        global quizzes
        for i in range(1, 5+1):  #TODO: вынести количество вопросов в .env
            quizzes[request.session.session_key]\
                .record_user_answer(request.POST.get("answer" + "-" + str(i)))
        answers = quizzes[request.session.session_key].get_user_answers()
        marks = quizzes[request.session.session_key].check_quiz()
        django.contrib.messages.success(request, "Квиз завершен!")
        return render(request, "quiz.html", context={"terms": quizzes[request.session.session_key].qna,
                                                     "quiz_start": False,
                                                     "answers": answers,
                                                     "marks": marks})
    return redirect("/quiz")
