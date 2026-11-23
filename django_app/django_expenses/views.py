from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Count
from decimal import Decimal
from .models import Transaction, Category, Budget
from django.utils import timezone
from django.contrib import messages
from .forms import ExpenseForm, IncomeForm, BudgetForm
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import TransactionSerializer
from drf_spectacular.utils import extend_schema

# =====================================================
# Статичні сторінки
# =====================================================


def home(request):
    # Отримуємо транзакції лише авторизованого користувача
    if request.user.is_authenticated:
        transactions = Transaction.objects.filter(
            user=request.user
        )
    else:
        transactions = Transaction.objects.none()

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
        context,
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
@login_required
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

@login_required
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

@login_required
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(
        Transaction,
        id=transaction_id,
    )

    if transaction.user != request.user:
        raise PermissionDenied("Доступ заборонено.")

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
@login_required
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

@login_required
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
@login_required
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

@login_required
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

@login_required
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

@login_required
def expense_update(request, transaction_id):
    """Редагування лише власної витрати."""

    expense = get_object_or_404(
        Transaction,
        id=transaction_id,
        transaction_type="expense",
    )

    if expense.user != request.user:
        raise PermissionDenied("Доступ заборонено.")

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Витрату успішно оновлено!"
            )

            return redirect("expense_list")
    else:
        form = ExpenseForm(instance=expense)

    context = {
        "title": "Редагування витрати",
        "form": form,
    }

    return render(
        request,
        "django_expenses/expense_form.html",
        context,
    )

@login_required
def expense_delete(request, transaction_id):
    """Видалення витрати."""

    expense = get_object_or_404(
        Transaction,
        id=transaction_id,
        user=request.user,
        transaction_type="expense",
    )

    if request.method == "POST":
        expense.delete()

        messages.success(
            request,
            "Витрату успішно видалено!"
        )

        return redirect("expense_list")

    context = {
        "title": "Видалення витрати",
        "expense": expense,
    }

    return render(
        request,
        "django_expenses/expense_confirm_delete.html",
        context,
    )

@login_required
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

@login_required
def income_create(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)

        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.transaction_type = "income"
            income.save()

            messages.success(request, "Дохід успішно додано!")
            return redirect("income_list")
    else:
        form = IncomeForm()

    context = {
        "title": "Додавання доходу",
        "form": form,
    }

    return render(
        request,
        "django_expenses/expense_form.html",
        context,
    )

@login_required
def budget_create(request):
    if request.method == "POST":
        form = BudgetForm(request.POST)

        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()

            messages.success(
                request,
                "Бюджет успішно створено!"
            )
            return redirect("budgets_list")

    else:
        form = BudgetForm()

    context = {
        "title": "Додавання бюджету",
        "form": form,
    }

    return render(
        request,
        "django_expenses/expense_form.html",
        context,
    )

@login_required
def budget_update(request, budget_id):
    budget = get_object_or_404(
        Budget,
        id=budget_id,
    )

    if budget.user != request.user:
        raise PermissionDenied("Доступ заборонено.")

    if request.method == "POST":
        form = BudgetForm(request.POST, instance=budget)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Бюджет успішно оновлено!"
            )
            return redirect("budgets_list")

    else:
        form = BudgetForm(instance=budget)

    context = {
        "title": "Редагування бюджету",
        "form": form,
    }

    return render(
        request,
        "django_expenses/expense_form.html",
        context,
    )
@login_required
def budget_delete(request, budget_id):
    budget = get_object_or_404(
        Budget,
        id=budget_id,
        user=request.user,
    )

    if request.method == "POST":
        budget.delete()

        messages.success(
            request,
            "Бюджет успішно видалено!"
        )
        return redirect("budgets_list")

    context = {
        "budget": budget,
        "title": "Видалення бюджету",
    }

    return render(
        request,
        "django_expenses/budget_confirm_delete.html",
        context,
    )

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Реєстрація успішна! Тепер увійдіть у свій акаунт."
            )

            return redirect("login")

    else:
        form = RegisterForm()

    context = {
        "title": "Реєстрація",
        "form": form,
    }

    return render(
        request,
        "django_expenses/register.html",
        context,
    )

@login_required
def profile(request):
    context = {
        "title": "Мій профіль",
        "profile_user": request.user,
    }

    return render(
        request,
        "django_expenses/profile.html",
        context,
    )

class TransactionListAPIView(APIView):
    """API для отримання та створення транзакцій."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=TransactionSerializer(many=True),
        description="Отримання списку транзакцій поточного користувача."
    )
    def get(self, request):
        transactions = Transaction.objects.filter(
            user=request.user
        )

        serializer = TransactionSerializer(
            transactions,
            many=True
        )

        return Response(serializer.data)

    @extend_schema(
        request=TransactionSerializer,
        responses={201: TransactionSerializer},
        description="Створення нової транзакції."
    )
    def post(self, request):
        serializer = TransactionSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class StatisticsAPIView(APIView):
    """API для отримання фінансової статистики користувача."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_transactions = Transaction.objects.filter(
            user=request.user
        )

        income_transactions = user_transactions.filter(
            transaction_type="income"
        )

        expense_transactions = user_transactions.filter(
            transaction_type="expense"
        )

        total_income = (
            income_transactions.aggregate(
                total=Sum("amount")
            )["total"] or Decimal("0.00")
        )

        total_expense = (
            expense_transactions.aggregate(
                total=Sum("amount")
            )["total"] or Decimal("0.00")
        )

        statistics = {
            "total_transactions": user_transactions.count(),
            "income_count": income_transactions.count(),
            "expense_count": expense_transactions.count(),
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": total_income - total_expense,
            "budgets_count": Budget.objects.filter(
                user=request.user
            ).count(),
        }

        return Response(statistics)
