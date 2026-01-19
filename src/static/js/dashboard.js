const explanations = {
    imbalance: "Checks if the target variable is highly imbalanced.",
    demo_bias: "Detects demographic bias using statistical tests.",
    representation: "Identifies underrepresented demographic groups.",
    correlation: "Checks correlations between features and protected attributes.",
    overfitting: "Warns about overfitting risks based on data structure.",
    leakage: "Detects possible data leakage features.",
    missing_values: "Analyzes missing data patterns.",
    outliers: "Detects extreme values that may affect the model."
};

function runCheck(endpoint, fileName) {
    const variable = document.getElementById("global_var")?.value;

    fetch(`/${endpoint}/${fileName}`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ var: variable })
    })
    .then(res => res.json())
    .then(data => renderResults(endpoint, data))
    .catch(err => {
        document.getElementById("resultsArea").innerHTML =
            `<p style="color:red;">${err}</p>`;
    });
}

function renderResults(check, data) {
    let html = `<p><strong>Description:</strong> ${explanations[check]}</p>`;

    for (const key in data) {
        const isSummary = key === "summary";

        html += `
            <div class="result-section ${isSummary ? "summary-section" : ""}">
                <div class="collapsible">
                    ${key}
                </div>
                <div class="content ${isSummary ? "summary-content" : ""}">
                    ${
                        isSummary
                            ? `<div class="summary-text">${data[key]}</div>`
                            : `<pre>${JSON.stringify(data[key], null, 2)}</pre>`
                    }
                </div>
            </div>
        `;
    }

    document.getElementById("resultsArea").innerHTML = html;
    enableCollapsible();
}

function enableCollapsible() {
    document.querySelectorAll(".collapsible").forEach(el => {
        el.addEventListener("click", () => {
            const content = el.nextElementSibling;
            if (content.style.maxHeight) {
                content.style.maxHeight = null;
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
            }
        });
    });
}