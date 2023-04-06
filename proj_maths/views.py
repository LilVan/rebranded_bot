from django.shortcuts import render
from django.core.cache import cache
from . import terms_work
import random
from .models import Doctors


def db_get_doctors():
    doctors = []
    for i, item in enumerate(Doctors.objects.all()):
        doctors.append([i+1, item.doctor_last_name, item.doctor_first_name])
    return doctors

def index(request):
    doctors = db_get_doctors()
    return render(request, "index.html", context={"d": doctors})


def terms_list(request):
    terms = terms_work.get_terms_for_table()
    return render(request, "term_list.html", context={"terms": terms})


def terms_list_new(request, slug):
    if slug == 'random':
        terms = terms_work.get_terms_for_table()
        terms = random.choice(terms)
    return render(request, "term_list.html", context={"terms": terms, "slug": slug})

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
