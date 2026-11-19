document.addEventListener("DOMContentLoaded", function () {
    console.log("Expense Tracker завантажився!");

    // Знаходимо всі елементи з класом amount
    const amounts = document.querySelectorAll(".amount");

    // Додаємо курсор при наведенні
    amounts.forEach(element => {
        element.style.cursor = "pointer";
    });
});
