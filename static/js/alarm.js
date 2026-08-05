// ==========================================
// SAFEPOSE AI
// alarm.js
// ==========================================

// Alarm Audio
const alarmAudio = new Audio("/static/alarm.mp3");

alarmAudio.loop = true;

// Prevent multiple alarms
let alarmPlaying = false;

// Store timeout reference
let alarmTimeout = null;

// ==============================
// PLAY ALARM
// ==============================

function playAlarm() {

    // Already playing
    if (alarmPlaying) return;

    alarmPlaying = true;

    alarmAudio.currentTime = 0;

    alarmAudio.play().catch(error => {
        console.log("Unable to play alarm:", error);
    });

    // Stop automatically after 3 seconds

    alarmTimeout = setTimeout(() => {

        stopAlarm();

    }, 3000);

}

// ==============================
// STOP ALARM
// ==============================

function stopAlarm() {

    if (alarmTimeout) {

        clearTimeout(alarmTimeout);

        alarmTimeout = null;

    }

    alarmAudio.pause();

    alarmAudio.currentTime = 0;

    alarmPlaying = false;

}