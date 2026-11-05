from expense_tracker.decorators import (
    validate_amount,
    currency_aware,
)


# Функція для перевірки validate_amount
@validate_amount
def process_amount(amount):
    return amount


# Функція для перевірки currency_aware
@currency_aware(base_currency="UAH")
def process_currency(amount):
    return amount


# ===== VALIDATE_AMOUNT =====

def test_valid_amount():
    assert process_amount(500) == 500


def test_zero_amount():
    assert process_amount(0) is None


def test_negative_amount():
    assert process_amount(-100) is None


def test_invalid_amount():
    assert process_amount("abc") is None


def test_boolean_amount():
    assert process_amount(True) is None


# ===== CURRENCY_AWARE =====

def test_currency_aware_returns_amount():
    assert process_currency(500) == 500
    