document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("uploadForm");
    const fileInput = document.getElementById("resumeInput");
    const feedbackDiv = document.getElementById("feedback");
    const loadingDiv = document.getElementById("loading");
    const resumeTextDiv = document.getElementById("resumeText");

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        if (!fileInput.files.length) {
            feedbackDiv.innerHTML = "<p style='color: red;'>❌ Please select a file.</p>";
            return;
        }

        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append("resume", file);

        feedbackDiv.innerHTML = "";
        loadingDiv.style.display = "block";
        resumeTextDiv.innerText = "";

        fetch("/analyze_resume", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loadingDiv.style.display = "none";
            if (data.error) {
                feedbackDiv.innerHTML = `<p style='color: red;'>❌ ${data.error}</p>`;
            } else {
                feedbackDiv.innerHTML = `<p style='color: green;'>✅ ${data.message}</p>`;
                resumeTextDiv.innerText = data.extracted_text;
                resumeTextDiv.style.display = "block"; // Ensure text is visible
            }
        })
        .catch(error => {
            loadingDiv.style.display = "none";
            feedbackDiv.innerHTML = "<p style='color: red;'>❌ Error analyzing resume.</p>";
            console.error("Error:", error);
        });
    });
});
