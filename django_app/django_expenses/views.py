from django.shortcuts import render


def home(request):
    context = {
        "title": "Головна",
        "message": "Вітаємо на сайті!",
    }
    return render(request, "django_expenses/home.html", context)

def about(request):
    context = {
        "title": "Про нас",
        "text": "Це сторінка з інформацією про проєкт.",
    }
    return render(request, "django_expenses/about.html", context)

def contacts(request):
    context = {
        "title": "Контакти",
        "email": "info@example.com",
        "phone": "+380 66 864 64 74",
    }
    return render(request, "django_expenses/contacts.html", context)
