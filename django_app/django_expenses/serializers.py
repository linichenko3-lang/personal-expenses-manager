from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """Серіалізатор для доходів і витрат."""

    class Meta:
        model = Transaction
        fields = [
            "id",
            "category",
            "amount",
            "transaction_type",
            "date",
            "description",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
