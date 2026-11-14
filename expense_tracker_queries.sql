-- 1. Великі витрати
-- Бізнес-питання: які витрати становлять 500 грн і більше?
-- Очікувано: приблизно 1–5 рядків.

SELECT
    id,
    date,
    category,
    amount,
    description
FROM transactions
WHERE transaction_type = 'expense'
    AND amount >= 500
ORDER BY amount DESC
LIMIT 10;


-- 2. Пошук транзакцій за описом
-- Бізнес-питання: які транзакції містять згадку про кафе?
-- Очікувано: приблизно 1–3 рядки.

SELECT
    id,
    date,
    transaction_type,
    category,
    amount,
    description
FROM transactions
WHERE description LIKE '%кафе%'
ORDER BY date DESC
LIMIT 10;

-- 3. Останні доходи
-- Бізнес-питання: які останні п'ять доходів були записані?
-- Очікувано: до 5 рядків.

SELECT
    id,
    date,
    category,
    amount,
    description
FROM transactions
WHERE transaction_type = 'income'
ORDER BY date DESC, id DESC
LIMIT 5;

-- 4. Пошук бюджетів за категорією
-- Бізнес-питання: які ліміти встановлено для категорії "Їжа"?
-- Очікувано: приблизно 2 рядки.

SELECT
    id,
    user_id,
    category,
    monthly_limit
FROM budgets
WHERE category LIKE '%Їжа%'
ORDER BY monthly_limit DESC
LIMIT 10;

-- 5. Транзакції та користувачі (INNER JOIN)
-- Бізнес-питання: хто здійснював кожну фінансову операцію?
-- Очікувано: приблизно 5–15 рядків.

SELECT
    t.id AS transaction_id,
    u.username,
    u.email,
    t.date,
    t.transaction_type,
    t.category,
    t.amount,
    t.description
FROM transactions AS t
INNER JOIN users AS u
    ON t.user_id = u.id
ORDER BY t.date DESC
LIMIT 20;

-- 6. Бюджети та користувачі (INNER JOIN)
-- Бізнес-питання: які бюджети встановив кожен користувач?
-- Очікувано: приблизно 3–8 рядків.

SELECT
    u.username,
    u.email,
    b.category,
    b.monthly_limit
FROM budgets AS b
INNER JOIN users AS u
    ON b.user_id = u.id
ORDER BY b.monthly_limit DESC;


-- 7. Користувачі та їхні транзакції (LEFT JOIN)
-- Бізнес-питання: скільки операцій має кожен користувач?
-- Очікувано: приблизно 3 рядки, по одному на користувача.

SELECT
    u.username,

    COUNT(t.id) AS transaction_count,

    COALESCE(
        SUM(
            CASE
                WHEN t.transaction_type = 'income'
                THEN t.amount
                ELSE 0
            END
        ), 0
    ) AS total_income,

    COALESCE(
        SUM(
            CASE
                WHEN t.transaction_type = 'expense'
                THEN t.amount
                ELSE 0
            END
        ), 0
    ) AS total_expenses

FROM users AS u

LEFT JOIN transactions AS t
    ON u.id = t.user_id

GROUP BY u.id, u.username

ORDER BY transaction_count DESC;

-- 8. Користувачі та бюджети (LEFT JOIN)
-- Бізнес-питання: скільки бюджетів має кожен користувач?
-- Очікувано: приблизно 3 рядки, по одному на користувача.

SELECT
    u.username,

    COUNT(b.id) AS budget_count,

    COALESCE(
        SUM(b.monthly_limit), 0
    ) AS total_budget

FROM users AS u

LEFT JOIN budgets AS b
    ON u.id = b.user_id

GROUP BY u.id, u.username

ORDER BY total_budget DESC;

-- 9. Користувачі без транзакцій (Anti JOIN)
-- Бізнес-питання: хто зареєструвався, але не користується обліком?
-- Очікувано: приблизно 0–2 рядки.

SELECT
    u.id,
    u.username,
    u.email
FROM users AS u

LEFT JOIN transactions AS t
    ON u.id = t.user_id

WHERE t.id IS NULL

ORDER BY u.username;

-- 10. Користувачі без бюджетів (Anti JOIN)
-- Бізнес-питання: хто ще не встановив собі фінансові ліміти?
-- Очікувано: приблизно 0–2 рядки.

SELECT
    u.id,
    u.username,
    u.email
FROM users AS u

LEFT JOIN budgets AS b
    ON u.id = b.user_id

WHERE b.id IS NULL

ORDER BY u.username;