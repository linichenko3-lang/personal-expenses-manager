from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Budget, Category

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
