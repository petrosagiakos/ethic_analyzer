function loadUploadedFiles() {
    fetch("/files")
        .then(res => res.json())
        .then(data => {
            let html = "<h3>Uploaded Files</h3>";

            data.files.forEach(file => {
                html += `
                    <div class="file-row">
                        <span>${file}</span>
                        <div class="file-actions">
                            <button onclick="reuseFile('${file}')">Reuse</button>
                            <button class="danger" onclick="deleteFile('${file}')">Delete</button>
                        </div>
                    </div>
                `;
            });

            document.getElementById("filesArea").innerHTML = html;
        });
}
function reuseFile(file) {
    window.location.href = `/preview/${file}`;
}

function deleteFile(file) {
    if (!confirm(`Delete ${file}?`)) return;

    fetch(`/files/${file}`, { method: "DELETE" })
        .then(res => res.json())
        .then(() => loadUploadedFiles());
}

document.addEventListener("DOMContentLoaded", () => {
    loadUploadedFiles();
});