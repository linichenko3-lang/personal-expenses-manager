from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Категорії доходів і видатків."""

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """Модель доходів і видатків."""

    TYPE_CHOICES = [
        ("income", "Дохід"),
        ("expense", "Видаток"),
    ]

    # Тимчасово допускаємо NULL для безпечної міграції
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transactions",
        null=True,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="transactions",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Сума в гривнях",
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
    )

    date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Транзакція"
        verbose_name_plural = "Транзакції"
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["user", "-date"]),
            models.Index(fields=["transaction_type"]),
        ]

    def __str__(self):
        return (
            f"{self.user.username if self.user else 'Без користувача'}"
            f" - {self.amount} ₴ "
            f"({self.get_transaction_type_display()})"
        )
    @classmethod
    def get_monthly_stats(cls, user, month, year):
        """Статистика доходів і витрат за місяць."""

        transactions = cls.objects.filter(
            user=user,
            date__month=month,
            date__year=year
        )

        income = transactions.filter(
            transaction_type="income"
        ).aggregate(
            total=models.Sum("amount")
        )["total"] or 0

        expense = transactions.filter(
            transaction_type="expense"
        ).aggregate(
            total=models.Sum("amount")
        )["total"] or 0

        return {
            "income": income,
            "expense": expense,
            "balance": income - expense
        }

    @classmethod
    def get_by_category(cls, user):
        """Витрати за категоріями."""

        return (
            cls.objects
            .filter(
                user=user,
                transaction_type="expense"
            )
            .values("category__name")
            .annotate(total=models.Sum("amount"))
            .order_by("-total")
        )


class Budget(models.Model):
    """Бюджет: ліміт видатків на місяць за категорією."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="budgets",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )

    month = models.IntegerField()
    year = models.IntegerField()

    limit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Максимальна сума видатків на місяць",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Бюджет"
        verbose_name_plural = "Бюджети"
        unique_together = ["user", "category", "month", "year"]
        ordering = ["-year", "-month"]

    def __str__(self):
        return (
            f"{self.user.username} - {self.category} "
            f"({self.month}/{self.year}): {self.limit} ₴"
        )

    def get_spent(self):
        """Скільки вже витрачено цього місяця за цією категорією."""

        spent = Transaction.objects.filter(
            user=self.user,
            category=self.category,
            transaction_type="expense",
            date__month=self.month,
            date__year=self.year,
        ).aggregate(total=models.Sum("amount"))["total"] or 0

        return spent

    def get_remaining(self):
        """Скільки ще можна витратити."""

        return self.limit - self.get_spent()

    def is_exceeded(self):
        """Чи перевищено ліміт."""

        return self.get_spent() > self.limit
