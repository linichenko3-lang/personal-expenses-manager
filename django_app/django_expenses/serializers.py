from rest_framework import serializers
from .models import Transaction



from rest_framework import serializers
from .models import Transaction, Category


class CategorySerializer(serializers.ModelSerializer):
    """Серіалізатор категорії."""

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "category_type",
            "description",
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

