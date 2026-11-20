from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from decimal import Decimal
from .models import Transaction, Category, Budget
from django.utils import timezone
from django.contrib import messages
from .forms import ExpenseForm

# =====================================================
# Статичні сторінки
# =====================================================

def home(request):
    # Отримуємо транзакції поточного користувача
    transactions = Transaction.objects.filter(user=request.user)

    # Рахуємо доходи
    total_income = (
        transactions
        .filter(transaction_type="income")
        .aggregate(total=Sum("amount"))["total"]
        or Decimal("0.00")
    )

    # Рахуємо витрати
    total_expense = (
        transactions
        .filter(transaction_type="expense")
        .aggregate(total=Sum("amount"))["total"]
        or Decimal("0.00")
    )

    # Рахуємо баланс
    balance = total_income - total_expense

    # Останні 5 транзакцій
    recent_transactions = transactions.order_by("-date")[:5]

    context = {
        "title": "Панель керування",
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "recent_transactions": recent_transactions,
    }

    return render(
        request,
        "django_expenses/home.html",
        context
    )


def about(request):
    context = {
        "title": "Про застосунок",
        "text": "Expense Tracker — застосунок для обліку доходів, витрат і бюджетів.",
    }

    return render(request, "django_expenses/about.html", context)

def contacts(request):
    context = {
        "title": "Контакти",
        "email": "info@example.com",
        "phone": "+380 66 864 64 74",
    }

    return render(request, "django_expenses/contacts.html", context)

# =====================================================
# Транзакції та бюджети
# =====================================================

def transactions_list(request):
    selected_category = request.GET.get("category")
    selected_type = request.GET.get("type")

    # Отримуємо транзакції з бази даних
    transactions = Transaction.objects.filter(user=request.user)

    # Фільтрація за категорією
    if selected_category:
        transactions = transactions.filter(
            category__name=selected_category
        )

    # Фільтрація за типом
    if selected_type:
        transactions = transactions.filter(
            transaction_type=selected_type
        )
    total = transactions.aggregate(
    total=Sum("amount")
        )["total"] or Decimal("0.00")
    # Список категорій
    categories = (
        Transaction.objects
        .filter(user=request.user)
        .values_list("category__name", flat=True)
        .distinct()
        .order_by("category__name")
    )

    context = {
        "title": "Мої транзакції",
        "transactions": transactions.order_by("-date"),
        "categories": categories,
        "selected_category": selected_category,
        "selected_type": selected_type,
        "total": total,
    }

    return render(
        request,
        "django_expenses/transactions_list.html",
        context
    )


def transaction_detail(request, transaction_id):
    transaction = get_object_or_404(
        Transaction,
        id=transaction_id,
        user=request.user,
    )

    context = {
        "transaction": transaction,
    }

    return render(
        request,
        "django_expenses/transaction_detail.html",
        context,
    )

def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(
        Transaction,
        id=transaction_id,
        user=request.user,
    )

    if request.method == "POST":
        transaction.amount = request.POST.get("amount")
        transaction.transaction_type = request.POST.get("transaction_type")
        transaction.description = request.POST.get("description")

        category_name = request.POST.get("category")
        transaction.category = get_object_or_404(
            Category,
            name=category_name,
        )

        transaction.save()

        return redirect("transactions_list")

    context = {
        "transaction": transaction,
        "categories": Category.objects.all(),
        "title": "Редагування транзакції",
    }

    return render(
        request,
        "django_expenses/edit_transaction.html",
        context,
    )

def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(
        Transaction,
        id=transaction_id,
        user=request.user,
    )

    if request.method == "POST":
        transaction.delete()
        return redirect("transactions_list")

    context = {
        "transaction": transaction,
        "title": "Видалення транзакції",
    }

    return render(
        request,
        "django_expenses/delete_transaction.html",
        context,
    )

def budgets_list(request):
    """Список бюджетів."""

    budgets = (
        Budget.objects
        .filter(user=request.user)
        .select_related("category")
    )

    context = {
        "title": "Бюджети",
        "budgets": budgets,
    }

    return render(
        request,
        "django_expenses/budgets_list.html",
        context,
    )

def income_list(request):
    """Список тільки доходів."""

    income_transactions = Transaction.objects.filter(
        user=request.user,
        transaction_type="income",
    )

    total = income_transactions.aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0.00")

    context = {
        "title": "Доходи",
        "transactions": income_transactions,
        "total": total,
        "categories": Category.objects.filter(transactions__user=request.user
        ).values_list("name", flat=True).distinct(),
        "selected_type": "income",
    }

    return render(
        request,
        "django_expenses/transactions_list.html",
        context,
    )


def expense_list(request):
    """Список тільки витрат."""

    expense_transactions = Transaction.objects.filter(
        user=request.user,
        transaction_type="expense",
    )

    total = expense_transactions.aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0.00")

    context = {
        "title": "Витрати",
        "transactions": expense_transactions,
        "total": total,
        "categories": Category.objects.filter(transactions__user=request.user
        ).values_list("name", flat=True).distinct(),
        "selected_type": "expense",
    }

    return render(
        request,
        "django_expenses/transactions_list.html",
        context,
    )

def expense_create(request):
    """Створення нової витрати."""

    if request.method == "POST":
        form = ExpenseForm(request.POST)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.transaction_type = "expense"
            expense.save()

            messages.success(
                request,
                "Витрату успішно додано!"
            )

            return redirect("expense_list")

    else:
        form = ExpenseForm()

    context = {
        "title": "Додавання витрати",
        "form": form,
    }

    return render(
        request,
        "django_expenses/expense_form.html",
        context,
    )

def monthly_report(request):
    selected_month = request.GET.get(
        "month",
        timezone.localdate().strftime("%Y-%m"),
    )

    year, month = map(int, selected_month.split("-"))

    monthly_transactions = Transaction.objects.filter(
        user=request.user,
        date__year=year,
        date__month=month,
    ).order_by("-date")

    total_income = (
        monthly_transactions
        .filter(transaction_type="income")
        .aggregate(total=Sum("amount"))["total"]
        or Decimal("0.00")
    )

    total_expense = (
        monthly_transactions
        .filter(transaction_type="expense")
        .aggregate(total=Sum("amount"))["total"]
        or Decimal("0.00")
    )

    balance = total_income - total_expense

    context = {
        "title": "Місячний звіт",
        "selected_month": selected_month,
        "transactions": monthly_transactions,
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
    }

    return render(
        request,
        "django_expenses/monthly_report.html",
        context,
    )