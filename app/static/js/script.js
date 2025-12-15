document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const btn = document.getElementById('submit-btn');
    const resultCard = document.getElementById('result-card');
    const qualityLabel = document.getElementById('quality-label');
    const latencyVal = document.querySelector('#latency span');

    btn.innerText = "Analyzing...";
    btn.disabled = true;

    // Build JSON payload from form
    const formData = new FormData(e.target);
    const payload = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        resultCard.classList.remove('hidden');
        qualityLabel.innerText = data.quality_label;
        qualityLabel.className = data.quality_label.includes('Good') ? 'good' : 'bad';
        latencyVal.innerText = data.latency_ms;

    } catch (error) {
        alert("Server connection failed!");
    } finally {
        btn.innerText = "Run Inference";
        btn.disabled = false;
    }
});