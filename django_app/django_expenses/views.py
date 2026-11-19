from django.shortcuts import render, redirect
from django.http import HttpResponse


# =====================================================
# Тимчасові дані для Expense Tracker
# =====================================================

TRANSACTIONS = [
    {
        "id": 1,
        "amount": 30000,
        "type": "income",
        "category": "Salary",
        "date": "2024-01-15",
        "description": "Зарплата за січень",
    },
    {
        "id": 2,
        "amount": 5000,
        "type": "expense",
        "category": "Food",
        "date": "2024-01-16",
        "description": "Продукти",
    },
    {
        "id": 3,
        "amount": 3000,
        "type": "expense",
        "category": "Transport",
        "date": "2024-01-17",
        "description": "Бензин",
    },
    {
        "id": 4,
        "amount": 15000,
        "type": "income",
        "category": "Freelance",
        "date": "2024-01-18",
        "description": "Проєкт для клієнта",
    },
]

BUDGETS = [
    {"category": "Food", "monthly_limit": 10000},
    {"category": "Transport", "monthly_limit": 5000},
    {"category": "Entertainment", "monthly_limit": 3000},
]


# =====================================================
# Статичні сторінки
# =====================================================

def home(request):
    total_income = sum(
        t["amount"] for t in TRANSACTIONS
        if t["type"] == "income"
    )

    total_expense = sum(
        t["amount"] for t in TRANSACTIONS
        if t["type"] == "expense"
    )

    balance = total_income - total_expense

    # Сортуємо транзакції за датою від нових до старих
    recent_transactions = sorted(
        TRANSACTIONS,
        key=lambda t: t["date"],
        reverse=True
    )[:5]

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
    # Отримуємо параметри фільтрації з URL
    selected_category = request.GET.get("category")
    selected_type = request.GET.get("type")

    transactions = TRANSACTIONS

    # Фільтрація за категорією
    if selected_category:
        transactions = [
            t for t in transactions
            if t["category"] == selected_category
        ]

    # Фільтрація за типом
    if selected_type:
        transactions = [
            t for t in transactions
            if t["type"] == selected_type
        ]

    categories = sorted({
        t["category"] for t in TRANSACTIONS
    })

    context = {
        "title": "Мої транзакції",
        "transactions": transactions,
        "categories": categories,
        "selected_category": selected_category,
        "selected_type": selected_type,
    }

    return render(
        request,
        "django_expenses/transactions_list.html",
        context
    )


def transaction_detail(request, transaction_id):
    """Деталі окремої транзакції."""

    transaction = next(
        (t for t in TRANSACTIONS if t["id"] == transaction_id),
        None
    )

    if transaction is None:
        return HttpResponse("Транзакція не знайдена", status=404)

    context = {"transaction": transaction}

    return render(
        request,
        "django_expenses/transaction_detail.html",
        context
    )

def edit_transaction(request, transaction_id):
    transaction = next(
        (t for t in TRANSACTIONS if t["id"] == transaction_id),
        None
    )

    if transaction is None:
        return HttpResponse("Транзакцію не знайдено", status=404)

    if request.method == "POST":
        transaction["amount"] = float(request.POST.get("amount"))
        transaction["category"] = request.POST.get("category")
        transaction["description"] = request.POST.get("description")

        return redirect("transactions_list")

    context = {
        "transaction": transaction,
        "title": "Редагування транзакції",
    }

    return render(
        request,
        "django_expenses/edit_transaction.html",
        context
    )

def delete_transaction(request, transaction_id):
    transaction = next(
        (t for t in TRANSACTIONS if t["id"] == transaction_id),
        None
    )

    if transaction is None:
        return HttpResponse("Транзакцію не знайдено", status=404)

    if request.method == "POST":
        TRANSACTIONS.remove(transaction)
        return redirect("transactions_list")

    context = {
        "transaction": transaction,
        "title": "Видалення транзакції",
    }

    return render(
        request,
        "django_expenses/delete_transaction.html",
        context
    )

def budgets_list(request):
    """Список бюджетів."""

    context = {
        "title": "Бюджети",
        "budgets": BUDGETS,
    }

    return render(
        request,
        "django_expenses/budgets_list.html",
        context
    )


def income_list(request):
    """Список тільки доходів."""

    income_transactions = [
        t for t in TRANSACTIONS
        if t["type"] == "income"
    ]

    total = sum(t["amount"] for t in income_transactions)

    context = {
        "title": "Доходи",
        "transactions": income_transactions,
        "total": total,
    }

    return render(
        request,
        "django_expenses/transactions_list.html",
        context
    )


def expense_list(request):
    """Список тільки витрат."""

    expense_transactions = [
        t for t in TRANSACTIONS
        if t["type"] == "expense"
    ]

    total = sum(t["amount"] for t in expense_transactions)

    context = {
        "title": "Витрати",
        "transactions": expense_transactions,
        "total": total,
    }

    return render(
        request,
        "django_expenses/transactions_list.html",
        context
    )

def monthly_report(request):
    selected_month = request.GET.get("month", "2024-01")

    monthly_transactions = [
        t for t in TRANSACTIONS
        if t["date"].startswith(selected_month)
    ]

    total_income = sum(
        t["amount"] for t in monthly_transactions
        if t["type"] == "income"
    )

    total_expense = sum(
        t["amount"] for t in monthly_transactions
        if t["type"] == "expense"
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
        context
    )

