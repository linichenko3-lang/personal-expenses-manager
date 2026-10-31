from expense_tracker.decorators import validate_amount
from expense_tracker.decorators import currency_aware



@validate_amount
def test_operation(amount):
    print(f"Операція виконана. Сума: {amount}")
    return amount


print("Тест 1:")
print(test_operation(500))

print("\nТест 2:")
print(test_operation(-100))

print("\nТест 3:")
print(test_operation("abc"))

@currency_aware(base_currency="UAH")
def test_currency(amount):
    print(f"Операція виконана. Сума: {amount}")
    return amount


print("\nТест 4:")
result = test_currency(500)
print("Результат:", result)
