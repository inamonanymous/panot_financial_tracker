(function (window) {
    function toDateInputValue(value) {
        if (!value || typeof value !== "string") {
            return "";
        }

        if (value.indexOf("T") !== -1) {
            return value.split("T")[0];
        }

        return value;
    }

    function resolveValue(value, fieldConfig) {
        if (!fieldConfig || !fieldConfig.type) {
            return value;
        }

        if (fieldConfig.type === "date") {
            return toDateInputValue(value);
        }

        return value;
    }

    function bindEditForm(options) {
        var editButtons = document.querySelectorAll(options.buttonSelector);
        var form = document.getElementById(options.formId);
        var submitButton = document.getElementById(options.submitButtonId);

        if (!form || !submitButton || editButtons.length === 0) {
            return;
        }

        var fields = {};
        var fieldKeys = Object.keys(options.fields || {});

        for (var i = 0; i < fieldKeys.length; i += 1) {
            var key = fieldKeys[i];
            var fieldId = options.fields[key].id;
            var element = document.getElementById(fieldId);

            if (!element) {
                return;
            }

            fields[key] = element;
        }

        function setLoadingState(isLoading) {
            submitButton.disabled = isLoading;
            for (var i = 0; i < fieldKeys.length; i += 1) {
                fields[fieldKeys[i]].disabled = isLoading;
            }
        }

        function resetFields() {
            for (var i = 0; i < fieldKeys.length; i += 1) {
                var key = fieldKeys[i];
                var defaultValue = "";
                if (options.defaults && Object.prototype.hasOwnProperty.call(options.defaults, key)) {
                    defaultValue = options.defaults[key];
                }
                fields[key].value = defaultValue;
            }
        }

        for (var i = 0; i < editButtons.length; i += 1) {
            editButtons[i].addEventListener("click", function (event) {
                event.preventDefault();

                var apiUrl = this.dataset[options.apiUrlDataKey];
                var updateUrl = this.dataset[options.updateUrlDataKey];

                if (!apiUrl || !updateUrl) {
                    return;
                }

                form.action = updateUrl;
                resetFields();
                setLoadingState(true);

                fetch(apiUrl, {
                    method: "GET",
                    headers: {
                        "Accept": "application/json"
                    }
                })
                    .then(function (response) {
                        if (!response.ok) {
                            throw new Error("Failed to fetch record");
                        }
                        return response.json();
                    })
                    .then(function (data) {
                        for (var j = 0; j < fieldKeys.length; j += 1) {
                            var key = fieldKeys[j];
                            var fieldConfig = options.fields[key];
                            var sourceKey = fieldConfig.source || key;
                            var value = data[sourceKey];
                            fields[key].value = resolveValue(value, fieldConfig) || "";
                        }
                    })
                    .catch(function () {
                        window.alert(options.errorMessage || "Unable to load record details. Please try again.");
                    })
                    .finally(function () {
                        setLoadingState(false);
                    });
            });
        }
    }

    window.EditFormHelper = {
        bindEditForm: bindEditForm
    };
}(window));
