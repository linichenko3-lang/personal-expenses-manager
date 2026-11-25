from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Budget, Category, Transaction

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch


class BudgetCRUDTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
        )

        self.category = Category.objects.create(
            name="Їжа",
            category_type="expense",
        )

        self.client.login(
            username="testuser",
            password="testpassword123",
        )

        self.budget = Budget.objects.create(
            user=self.user,
            category=self.category,
            month=11,
            year=2026,
            limit=Decimal("5000.00"),
        )

    def test_budget_create_valid(self):
        response = self.client.post(
            reverse("budget_create"),
            {
                "category": self.category.id,
                "month": 12,
                "year": 2026,
                "limit": "6000.00",
            },
        )

        self.assertRedirects(
            response,
            reverse("budgets_list"),
        )

        self.assertEqual(Budget.objects.count(), 2)

    def test_budget_create_invalid(self):
        response = self.client.post(
            reverse("budget_create"),
            {
                "category": self.category.id,
                "month": 15,
                "year": 2026,
                "limit": "6000.00",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Budget.objects.count(), 1)
        self.assertFormError(
            response.context["form"],
            "month",
            "Місяць повинен бути від 1 до 12.",
        )

    def test_budget_update(self):
        response = self.client.post(
            reverse(
                "budget_update",
                args=[self.budget.id],
            ),
            {
                "category": self.category.id,
                "month": 11,
                "year": 2026,
                "limit": "7000.00",
            },
        )

        self.assertRedirects(
            response,
            reverse("budgets_list"),
        )

        self.budget.refresh_from_db()
        self.assertEqual(
            self.budget.limit,
            Decimal("7000.00"),
        )

    def test_budget_update_404(self):
        response = self.client.get(
            reverse("budget_update", args=[99999])
        )

        self.assertEqual(response.status_code, 404)

    def test_budget_delete_get(self):
        response = self.client.get(
            reverse(
                "budget_delete",
                args=[self.budget.id],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Budget.objects.filter(id=self.budget.id).exists()
        )

    def test_budget_delete_post(self):
        response = self.client.post(
            reverse(
                "budget_delete",
                args=[self.budget.id],
            )
        )

        self.assertRedirects(
            response,
            reverse("budgets_list"),
        )

        self.assertFalse(
            Budget.objects.filter(id=self.budget.id).exists()
        )

User = get_user_model()


class TransactionAPITests(APITestCase):

    def setUp(self):
        # Створюємо тестового користувача
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )

        # Авторизуємо користувача
        self.client.force_authenticate(user=self.user)

        # Створюємо категорію
        self.category = Category.objects.create(
            name="Їжа",
            category_type="expense"
        )

        # URL списку транзакцій
        self.list_url = reverse("transaction-list")

        # Дані для створення транзакції
        self.transaction_data = {
            "category": self.category.id,
            "amount": "500.00",
            "transaction_type": "expense",
            "date": "2026-11-24",
            "description": "Покупки продуктів"
        }

    def test_transaction_list_returns_200(self):
        """Список транзакцій повертає HTTP 200."""
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_transaction_create_returns_201(self):
        """Створення транзакції повертає HTTP 201."""
        response = self.client.post(
            self.list_url,
            self.transaction_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)

    def test_transaction_create_without_required_field_returns_400(self):
        """Створення без обов'язкового поля повертає HTTP 400."""
        invalid_data = self.transaction_data.copy()
        invalid_data.pop("amount")

        response = self.client.post(
            self.list_url,
            invalid_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_transaction_patch_changes_only_sent_field(self):
        """PATCH змінює лише передане поле."""
        transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount="500.00",
            transaction_type="expense",
            date="2026-11-24",
            description="Покупки продуктів"
        )

        detail_url = reverse(
            "transaction-detail",
            args=[transaction.id]
        )

        response = self.client.patch(
            detail_url,
            {"amount": "700.00"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        transaction.refresh_from_db()

        self.assertEqual(str(transaction.amount), "700.00")
        self.assertEqual(transaction.description, "Покупки продуктів")
        self.assertEqual(transaction.transaction_type, "expense")

    def test_transaction_delete_returns_204_and_get_returns_404(self):
        """DELETE повертає 204, наступний GET повертає 404."""
        transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount="500.00",
            transaction_type="expense",
            date="2026-11-24",
            description="Покупки продуктів"
        )

        detail_url = reverse(
            "transaction-detail",
            args=[transaction.id]
        )

        delete_response = self.client.delete(detail_url)

        self.assertEqual(
            delete_response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        get_response = self.client.get(detail_url)

        self.assertEqual(
            get_response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_transaction_list_requires_authentication(self):
        """Без авторизації API повертає 401."""
        self.client.force_authenticate(user=None)

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_transaction_filter_by_income(self):
        """Фільтрація повертає лише доходи."""
        Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount="1000.00",
            transaction_type="income",
            date="2026-11-24",
            description="Зарплата"
        )

        Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount="300.00",
            transaction_type="expense",
            date="2026-11-24",
            description="Покупки"
        )

        response = self.client.get(
            self.list_url,
            {"transaction_type": "income"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["transaction_type"],
            "income"
        )

    def test_user_sees_only_own_transactions(self):
        """Користувач бачить лише власні транзакції."""
        other_user = User.objects.create_user(
            username="otheruser",
            password="testpassword123"
        )

        Transaction.objects.create(
            user=other_user,
            category=self.category,
            amount="900.00",
            transaction_type="expense",
            date="2026-11-24",
            description="Чужа покупка"
        )

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_user_cannot_retrieve_foreign_transaction(self):
        """Користувач не може переглянути чужу транзакцію."""
        other_user = User.objects.create_user(
            username="otheruser",
            password="testpassword123"
        )

        transaction = Transaction.objects.create(
            user=other_user,
            category=self.category,
            amount="900.00",
            transaction_type="expense",
            date="2026-11-24",
            description="Чужа покупка"
        )

        detail_url = reverse(
            "transaction-detail",
            args=[transaction.id]
        )

        response = self.client.get(detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    @patch("django_expenses.views.send_budget_exceeded_notification")
    def test_webhook_called_when_budget_exceeded(self, mock_webhook):
        """Webhook викликається, коли витрати перевищують бюджет."""

        budget = Budget.objects.create(
            user=self.user,
            category=self.category,
            month=11,
            year=2026,
            limit=Decimal("1000.00"),
        )

        transaction_data = self.transaction_data.copy()
        transaction_data["amount"] = "1200.00"

        response = self.client.post(
            self.list_url,
            transaction_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        mock_webhook.assert_called_once()

        called_budget = mock_webhook.call_args[0][0]
        self.assertEqual(called_budget.id, budget.id)

    @patch("django_expenses.views.send_budget_exceeded_notification")
    def test_webhook_not_called_when_budget_not_exceeded(self, mock_webhook):
        """Webhook не викликається, якщо бюджет не перевищено."""

        Budget.objects.create(
            user=self.user,
            category=self.category,
            month=11,
            year=2026,
            limit=Decimal("1000.00"),
        )

        response = self.client.post(
            self.list_url,
            self.transaction_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        mock_webhook.assert_not_called()
