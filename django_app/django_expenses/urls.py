from django.urls import path
from . import views

urlpatterns = [
    # Статичні сторінки
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contacts/", views.contacts, name="contacts"),

    # Транзакції
    path("transactions/", views.transactions_list, name="transactions_list"),
    path(
        "transactions/<int:transaction_id>/",
        views.transaction_detail,
        name="transaction_detail"
    ),

    # Доходи та витрати
    path("income/", views.income_list, name="income_list"),
    path("expenses/", views.expense_list, name="expense_list"),
    path("monthly-report/", views.monthly_report, name="monthly_report"),

    # Бюджети
    path("budgets/", views.budgets_list, name="budgets_list"),
]