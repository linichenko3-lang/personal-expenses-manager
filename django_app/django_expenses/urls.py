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
    path("transactions/<int:transaction_id>/edit/", views.edit_transaction, name="edit_transaction"),
    path("transactions/<int:transaction_id>/delete/", views.delete_transaction, name="delete_transaction"),
    path("expenses/create/", views.expense_create, name="expense_create"),
    path("expenses/<int:transaction_id>/edit/", views.expense_update, name="expense_update"),
    path("expenses/<int:transaction_id>/delete/", views.expense_delete, name="expense_delete"),
    path("income/create/", views.income_create, name="income_create"),
    path("budgets/create/", views.budget_create, name="budget_create"),
]