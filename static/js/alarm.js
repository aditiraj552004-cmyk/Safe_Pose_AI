// ===============================
// alarm.js
// ===============================

// Alarm sound
let alarmSound = new Audio("/static/alarm.mp3");
alarmSound.loop = true;

// Alarm state
let alarmPlaying = false;

// -------------------------------
// Show Alarm
// -------------------------------
function showAlarm() {

    const alarmBox = document.getElementById("alarm");

    alarmBox.style.display = "block";

    if (!alarmPlaying) {

        alarmPlaying = true;

        alarmSound.currentTime = 0;

        alarmSound.play()
        .then(() => {
            console.log("Alarm Started");
        })
        .catch(error => {
            console.log("Alarm Play Error:", error);
        });

    }
}

// -------------------------------
// Hide Alarm
// -------------------------------
function hideAlarm() {

    const alarmBox = document.getElementById("alarm");

    alarmBox.style.display = "none";

    if (alarmPlaying) {

        alarmSound.pause();
        alarmSound.currentTime = 0;
        alarmPlaying = false;

        console.log("Alarm Stopped");

    }
}

// -------------------------------
// Reset Alarm
// -------------------------------
function resetAlarm() {

    fetch("/reset_alarm")

    .then(response => response.json())

    .then(data => {

        console.log(data.message);

        hideAlarm();

    })

    .catch(error => {

        console.log("Reset Error:", error);

    });

}