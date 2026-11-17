from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def home(request):
    return HttpResponse("Вітаю тебе, Django!")

def about(request):
    """Сторінка про застосунок."""
    return render(request, "django_expenses/about.html")