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
        buttonSelector: ".js-edit-income-btn",
        formId: "editIncomeForm",
        submitButtonId: "editIncomeSubmit",
        apiUrlDataKey: "incomeApiUrl",
        updateUrlDataKey: "incomeUpdateUrl",
        errorMessage: "Unable to load income details. Please try again.",
        defaults: {
            category_id: "",
            name: "",
            source: "",
            amount: "",
            received_date: "",
            payment_method: "cash",
            remarks: ""
        },
        fields: {
            category_id: { id: "edit_income_category_id", source: "category_id" },
            name: { id: "edit_income_name", source: "name" },
            source: { id: "edit_income_source", source: "source" },
            amount: { id: "edit_income_amount", source: "amount" },
            received_date: { id: "edit_income_received_date", source: "received_date", type: "date" },
            payment_method: { id: "edit_income_method", source: "payment_method" },
            remarks: { id: "edit_income_remarks", source: "remarks" }
        }
    });
});
