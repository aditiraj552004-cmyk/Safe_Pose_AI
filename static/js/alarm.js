// ===============================
// ALARM SOUND
// ===============================

const alarm = new Audio("/static/alarm.mpeg");

// Loop the alarm until reset
alarm.loop = true;

let alarmPlaying = false;

// ===============================
// CHECK FALL STATUS
// ===============================

async function checkAlarm() {

    try {

        const response = await fetch("/status");
        const data = await response.json();

        if (data.alarm) {

            if (!alarmPlaying) {

                alarm.play().catch(err => {
                    console.log("Audio blocked:", err);
                });

                alarmPlaying = true;
            }

        } else {

            if (alarmPlaying) {

                alarm.pause();
                alarm.currentTime = 0;

                alarmPlaying = false;
            }

        }

    } catch (err) {

        console.log(err);

    }

}

// ===============================
// CHECK EVERY SECOND
// ===============================

setInterval(checkAlarm, 1000);

checkAlarm();