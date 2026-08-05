// ========================================
// SAFEPOSE AI - app.js
// ========================================

// HTML Elements
const predictionText = document.getElementById("prediction");
const confidenceText = document.getElementById("confidenceText");
const progressBar = document.getElementById("progressBar");

const popup = document.getElementById("popup");
const alertCard = document.getElementById("alertCard");
const alarmStatus = document.getElementById("alarmStatus");

const resetBtn = document.getElementById("resetBtn");

// Prevent repeated popup/alarm
let popupVisible = false;

// ===============================
// GET STATUS FROM FLASK
// ===============================

async function updateStatus() {

    try {

        const response = await fetch("/status");

        const data = await response.json();

        // --------------------------
        // Prediction
        // --------------------------

        predictionText.innerText = data.prediction;

        // --------------------------
        // Confidence
        // --------------------------

        confidenceText.innerText =
            data.confidence.toFixed(1) + "%";

        progressBar.style.width =
            data.confidence + "%";

        // Progress bar color

        if (data.confidence >= 80) {

            progressBar.style.background =
                "linear-gradient(90deg,#ef4444,#ff0000)";

        }
        else {

            progressBar.style.background =
                "linear-gradient(90deg,#00d2ff,#00ff88)";
        }

        // --------------------------
        // FALL DETECTED
        // --------------------------

        if (data.alarm) {

            predictionText.style.color = "#ff4444";

            alarmStatus.innerText = "FALL DETECTED";

            alarmStatus.className = "danger";

            alertCard.classList.add("alert-active");

            if (!popupVisible) {

                popupVisible = true;

                popup.classList.add("show");

                playAlarm();

                // Hide popup after 3 sec

                setTimeout(() => {

                    popup.classList.remove("show");

                    popupVisible = false;

                }, 3000);

            }

        }

        // --------------------------
        // NORMAL
        // --------------------------

        else {

            predictionText.style.color = "#22c55e";

            alarmStatus.innerText = "SAFE";

            alarmStatus.className = "safe";

            alertCard.classList.remove("alert-active");

            popup.classList.remove("show");

            stopAlarm();

            popupVisible = false;

        }

    }

    catch (error) {

        console.log(error);

    }

}

// ========================================
// UPDATE EVERY SECOND
// ========================================

setInterval(updateStatus, 1000);

updateStatus();

// ========================================
// RESET BUTTON
// ========================================

resetBtn.addEventListener("click", async () => {

    await fetch("/reset_alarm");

    popup.classList.remove("show");

    stopAlarm();

    popupVisible = false;

    updateStatus();

});