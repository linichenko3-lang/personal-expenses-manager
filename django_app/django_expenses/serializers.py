from rest_framework import serializers
from .models import Transaction



from rest_framework import serializers
from .models import Transaction, Category, Budget

class CategorySerializer(serializers.ModelSerializer):
    """Серіалізатор категорії."""

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "category_type",
            "icon",
        ]


class TransactionSerializer(serializers.ModelSerializer):
    """Серіалізатор транзакції з вкладеною категорією."""

    category_info = CategorySerializer(
        source="category",
        read_only=True
    )

    class Meta:
        model = Transaction
        fields = [
            "id",
            "category",
            "category_info",
            "amount",
            "transaction_type",
            "date",
            "description",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class BudgetSerializer(serializers.ModelSerializer):
    """Серіалізатор для бюджетів."""

    class Meta:
        model = Budget
        fields = [
            "id",
            "category",
            "month",
            "year",
            "limit",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

class StatisticsSerializer(serializers.Serializer):
    total_transactions = serializers.IntegerField()
    income_count = serializers.IntegerField()
    expense_count = serializers.IntegerField()
    total_income = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    total_expense = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    balance = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    budgets_count = serializers.IntegerField()

