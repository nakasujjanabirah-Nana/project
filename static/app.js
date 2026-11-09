async function getJson(url) {
    const response = await fetch(url);
    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.error || "The request could not be completed.");
    }
    return data;
}

function optionLabel(record, fields) {
    return fields
        .map((field) => record[field])
        .filter((value) => value !== undefined && value !== null && value !== "")
        .join(" - ");
}

async function loadOptions(select) {
    const records = await getJson(select.dataset.options);
    const valueField = select.dataset.valueField;
    const labelFields = select.dataset.labelFields.split(",");
    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = records.length ? "Select an option" : "No options available";
    select.replaceChildren(placeholder);

    for (const record of records) {
        const option = document.createElement("option");
        option.value = record[valueField] ?? "";
        option.textContent = optionLabel(record, labelFields);
        select.append(option);
    }
}

function renderRecords(container, records) {
    if (!records.length) {
        container.textContent = "No records saved yet.";
        return;
    }

    const columns = [...new Set(records.flatMap((record) => Object.keys(record)))];
    const table = document.createElement("table");
    const head = table.createTHead().insertRow();
    for (const column of columns) {
        const cell = document.createElement("th");
        cell.scope = "col";
        cell.textContent = column.replaceAll("_", " ");
        head.append(cell);
    }

    const body = table.createTBody();
    for (const record of records) {
        const row = body.insertRow();
        for (const column of columns) {
            const cell = row.insertCell();
            const value = record[column];
            cell.textContent = value === undefined || value === null ? "" : String(value);
        }
    }
    container.replaceChildren(table);
}

async function refreshRecords(container) {
    const records = await getJson(container.dataset.endpoint);
    renderRecords(container, records);
}

for (const select of document.querySelectorAll("select[data-options]")) {
    loadOptions(select).catch((error) => {
        const label = select.closest("label");
        if (label) {
            label.append(` ${error.message}`);
        }
    });
}

for (const container of document.querySelectorAll("[data-records]")) {
    refreshRecords(container).catch((error) => {
        container.textContent = error.message;
    });
}

for (const form of document.querySelectorAll("form[data-endpoint]")) {
    const message = form.querySelector("[data-form-message]");
    const typeSelect = form.elements.namedItem("transaction_type");
    const transferField = form.querySelector("[data-transfer-field]");

    if (typeSelect && transferField) {
        const receiver = form.elements.namedItem("receiver_account");
        const updateTransferField = () => {
            const isTransfer = typeSelect.value === "transfer";
            transferField.hidden = !isTransfer;
            receiver.required = isTransfer;
        };
        typeSelect.addEventListener("change", updateTransferField);
        updateTransferField();
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        message.textContent = "Saving...";
        const submitButton = form.querySelector('button[type="submit"]');
        submitButton.disabled = true;

        try {
            const payload = Object.fromEntries(new FormData(form).entries());
            const response = await fetch(form.dataset.endpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });
            const result = await response.json();
            if (!response.ok) {
                throw new Error(result.error || "The request could not be completed.");
            }

            message.textContent = "Saved successfully.";
            form.reset();
            if (typeSelect && transferField) {
                transferField.hidden = true;
                form.elements.namedItem("receiver_account").required = false;
            }
            await Promise.all(
                [...document.querySelectorAll("[data-records]")].map(refreshRecords),
            );
        } catch (error) {
            message.textContent = error.message;
        } finally {
            submitButton.disabled = false;
        }
    });
}