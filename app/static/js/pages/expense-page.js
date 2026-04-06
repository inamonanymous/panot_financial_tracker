document.addEventListener("DOMContentLoaded", function () {
    if (!window.EditFormHelper) {
        return;
    }

    window.EditFormHelper.bindEditForm({
        buttonSelector: ".js-edit-category-btn",
        formId: "editCategoryForm",
        submitButtonId: "editCategorySubmit",
        apiUrlDataKey: "categoryApiUrl",
        updateUrlDataKey: "categoryUpdateUrl",
        errorMessage: "Unable to load category details. Please try again.",
        defaults: {
            name: "",
            description: ""
        },
        fields: {
            name: { id: "editCategoryName", source: "name" },
            description: { id: "editCategoryDescription", source: "description" }
        }
    });

    window.EditFormHelper.bindEditForm({
        buttonSelector: ".js-edit-expense-btn",
        formId: "editExpenseForm",
        submitButtonId: "editExpenseSubmit",
        apiUrlDataKey: "expenseApiUrl",
        updateUrlDataKey: "expenseUpdateUrl",
        errorMessage: "Unable to load expense details. Please try again.",
        defaults: {
            category_id: "",
            name: "",
            payee: "",
            amount: "",
            expense_date: "",
            payment_method: "cash",
            remarks: ""
        },
        fields: {
            category_id: { id: "edit_expense_category_id", source: "category_id" },
            name: { id: "edit_expense_name", source: "name" },
            payee: { id: "edit_expense_payee", source: "payee" },
            amount: { id: "edit_expense_amount", source: "amount" },
            expense_date: { id: "edit_expense_date", source: "expense_date", type: "date" },
            payment_method: { id: "edit_expense_method", source: "payment_method" },
            remarks: { id: "edit_expense_remarks", source: "remarks" }
        }
    });
});
