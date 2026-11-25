import requests

from django.conf import settings


def send_budget_exceeded_notification(budget):
    """Надсилає webhook, якщо бюджет перевищено."""

    webhook_url = getattr(settings, "BUDGET_WEBHOOK_URL", None)

    if not webhook_url:
        return False

    payload = {
        "event": "budget_exceeded",
        "username": budget.user.username,
        "category": budget.category.name,
        "month": budget.month,
        "year": budget.year,
        "budget_limit": str(budget.limit),
        "spent": str(budget.get_spent()),
        "remaining": str(budget.get_remaining()),
    }

    try:
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        return True

    except requests.RequestException:
        return False
