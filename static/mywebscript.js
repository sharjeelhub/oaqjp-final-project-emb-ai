function RunSentimentAnalysis() {
    const textArea = document.getElementById("textToAnalyze");
    const responseDiv = document.getElementById("system_response");
    const spinner = document.querySelector(".loading-spinner");
    
    // Clear previous results
    responseDiv.innerHTML = "";
    responseDiv.className = "emotion-display";
    
    // Validate input
    const textToAnalyze = textArea.value.trim();
    if (!textToAnalyze) {
        responseDiv.innerHTML = `<div class="alert alert-danger">Please enter some text to analyze!</div>`;
        textArea.focus();
        return;
    }

    // Show loading spinner
    spinner.style.display = "block";

    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4) {
            spinner.style.display = "none";
            
            try {
                const response = JSON.parse(this.responseText);
                
                if (response.error) {
                    responseDiv.innerHTML = `
                        <div class="alert alert-danger">
                            <strong>Error:</strong> ${response.error}
                        </div>
                    `;
                } else {
                    responseDiv.innerHTML = `
                        <div class="alert alert-success">
                            ${response.response.replace(/\./g, '.<br>')}
                        </div>
                    `;
                    responseDiv.classList.add("bg-light", "p-3");
                }
            } catch (e) {
                responseDiv.innerHTML = `
                    <div class="alert alert-warning">
                        Failed to process response. Please try again.
                    </div>
                `;
            }
        }
    };

    xhttp.open("GET", `emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`);
    xhttp.send();
}

function loadSampleText() {
    const sampleText = "I'm absolutely thrilled about this new opportunity! It's exactly what I've been hoping for, though I must admit I feel a tiny bit nervous about the challenges ahead.";
    document.getElementById("textToAnalyze").value = sampleText;
    RunSentimentAnalysis();
}