from django.contrib import admin
from .models import Category, Transaction, Budget

admin.site.site_header = "Expense Tracker — Адміністрування"
admin.site.site_title = "Expense Tracker"
admin.site.index_title = "Керування фінансами"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category_type",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )

    list_filter = (
        "category_type",
        "created_at",
    )

    ordering = ("name",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "category",
        "transaction_type",
        "amount",
        "date",
    )

    search_fields = (
        "user__username",
        "category__name",
        "description",
    )

    list_filter = (
        "transaction_type",
        "category",
        "date",
    )

    ordering = ("-date",)


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "category",
        "month",
        "year",
        "limit",
    )

    search_fields = (
        "user__username",
        "category__name",
    )

    list_filter = (
        "month",
        "year",
        "category",
    )

    ordering = ("-year", "-month")
