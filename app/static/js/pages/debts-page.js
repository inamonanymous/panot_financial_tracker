document.addEventListener("DOMContentLoaded", function () {
    if (!window.EditFormHelper) {
        return;
    }

    window.EditFormHelper.bindEditForm({
        buttonSelector: ".js-edit-debt-btn",
        formId: "editDebtForm",
        submitButtonId: "editDebtSubmit",
        apiUrlDataKey: "debtApiUrl",
        updateUrlDataKey: "debtUpdateUrl",
        errorMessage: "Unable to load debt details. Please try again.",
        defaults: {
            name: "",
            lender: "",
            principal: "",
            interest_rate: ""
        },
        fields: {
            name: { id: "edit_debt_name", source: "name" },
            lender: { id: "edit_debt_lender", source: "lender" },
            principal: { id: "edit_debt_principal", source: "principal" },
            interest_rate: { id: "edit_debt_interest_rate", source: "interest_rate" }
        }
    });
});
