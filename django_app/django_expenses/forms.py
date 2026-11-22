from django import forms
from .models import Transaction, Category, Budget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ExpenseForm(forms.ModelForm):
    """Форма для створення та редагування витрат."""

    class Meta:
        model = Transaction

        fields = [
            "amount",
            "category",
            "date",
            "description",
        ]

        labels = {
            "amount": "Сума витрати (грн)",
            "category": "Категорія",
            "date": "Дата",
            "description": "Опис",
        }

        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "placeholder": "Введіть суму витрати",
                    "step": "0.01",
                    "min": "0.01",
                }
            ),
            "category": forms.Select(),
            "date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Напишіть опис витрати",
                    "rows": 3,
                }
            ),
        }

    def clean_amount(self):
        """Перевіряємо, що сума витрати більша за нуль."""

        amount = self.cleaned_data["amount"]

        if amount <= 0:
            raise forms.ValidationError(
                "Сума витрати повинна бути більшою за нуль."
            )

        return amount
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(
            category_type="expense"
        )

class IncomeForm(forms.ModelForm):
    """Форма для створення та редагування доходів."""

    class Meta:
        model = Transaction
        fields = [
            "amount",
            "category",
            "date",
            "description",
        ]
        labels = {
            "amount": "Сума доходу (грн)",
            "category": "Категорія",
            "date": "Дата",
            "description": "Опис",
        }
        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "placeholder": "Введіть суму доходу",
                    "step": "0.01",
                    "min": "0.01",
                }
            ),
            "category": forms.Select(),
            "date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Напишіть опис доходу",
                    "rows": 3,
                }
            ),
        }

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError(
                "Сума доходу повинна бути більшою за нуль."
            )
        return amount

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(
            category_type="income"
       )

class BudgetForm(forms.ModelForm):
    """Форма для створення та редагування бюджету."""

    class Meta:
        model = Budget
        fields = [
            "category",
            "month",
            "year",
            "limit",
        ]

        labels = {
            "category": "Категорія витрат",
            "month": "Місяць",
            "year": "Рік",
            "limit": "Місячний ліміт (грн)",
        }

        widgets = {
            "category": forms.Select(),
            "month": forms.NumberInput(
                attrs={
                    "placeholder": "Введіть номер місяця (1–12)",
                    "min": "1",
                    "max": "12",
                }
            ),
            "year": forms.NumberInput(
                attrs={
                    "placeholder": "Наприклад, 2026",
                }
            ),
            "limit": forms.NumberInput(
                attrs={
                    "placeholder": "Введіть суму бюджету",
                    "step": "0.01",
                    "min": "0.01",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(
            category_type="expense"
        )

    def clean_month(self):
        month = self.cleaned_data["month"]

        if not 1 <= month <= 12:
            raise forms.ValidationError(
                "Місяць повинен бути від 1 до 12."
            )

        return month

    def clean_limit(self):
        limit = self.cleaned_data["limit"]

        if limit <= 0:
            raise forms.ValidationError(
                "Бюджет повинен бути більшим за нуль."
            )

        return limit


class RegisterForm(UserCreationForm):
    """Форма реєстрації нового користувача."""

    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
        ]

        labels = {
            "username": "Логін",
            "password1": "Пароль",
            "password2": "Підтвердження пароля",
        }

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Введіть логін",
                }
            ),
        }
