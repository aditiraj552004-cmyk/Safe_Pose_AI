// ===============================
// ELEMENTS
// ===============================

const prediction = document.getElementById("prediction");
const confidence = document.getElementById("confidence");
const progressBar = document.getElementById("progressBar");
const historyBody = document.getElementById("historyBody");
const popup = document.getElementById("popup");

// ===============================
// CHART
// ===============================

const ctx = document.getElementById("confidenceChart").getContext("2d");

const confidenceChart = new Chart(ctx, {
    type: "line",
    data: {
        labels: [],
        datasets: [{
            label: "Confidence %",
            data: [],
            borderColor: "#38bdf8",
            backgroundColor: "rgba(56,189,248,0.2)",
            borderWidth: 3,
            tension: 0.4,
            fill: true
        }]
    },
    options: {
        responsive: true,
        animation: true,
        scales: {
            y: {
                min: 0,
                max: 100
            }
        }
    }
});

// ===============================
// UPDATE STATUS
// ===============================

async function updateStatus() {

    const response = await fetch("/status");
    const data = await response.json();

    prediction.innerHTML = data.prediction;

    confidence.innerHTML = data.confidence + "%";

    progressBar.style.width = data.confidence + "%";

    if (data.prediction === "FALL DETECTED") {

        prediction.style.color = "red";

        popup.style.display = "block";

    } else {

        prediction.style.color = "#22c55e";

        popup.style.display = "none";
    }

    // Chart

    const time = new Date().toLocaleTimeString();

    confidenceChart.data.labels.push(time);

    confidenceChart.data.datasets[0].data.push(data.confidence);

    if (confidenceChart.data.labels.length > 15) {

        confidenceChart.data.labels.shift();

        confidenceChart.data.datasets[0].data.shift();
    }

    confidenceChart.update();

}

// ===============================
// LOAD HISTORY
// ===============================

async function loadHistory() {

    const response = await fetch("/history");

    const data = await response.json();

    historyBody.innerHTML = "";

    data.reverse().forEach(item => {

        historyBody.innerHTML += `

        <tr>

            <td>${item.Time}</td>

            <td>${item["Confidence (%)"] || item.Confidence}%</td>

            <td>${item.Status}</td>

        </tr>

        `;

    });

}

// ===============================
// AUTO UPDATE
// ===============================

setInterval(() => {

    updateStatus();

    loadHistory();

}, 1000);

updateStatus();

loadHistory();