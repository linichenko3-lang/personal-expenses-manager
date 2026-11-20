from django import forms
from .models import Transaction


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
