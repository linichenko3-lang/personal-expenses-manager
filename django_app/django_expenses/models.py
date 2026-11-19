from django.db import models


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("income", "Дохід"),
        ("expense", "Витрата"),
    ]

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES
    )
    category = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.category}: {self.amount} грн"
