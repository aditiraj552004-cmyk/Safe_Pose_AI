// alarm.js



let alarmSound = new Audio(
    "/static/alarm.mp3"
);



// Prevent multiple alarms

let alarmPlaying = false;



function showAlarm(){


    let alarmBox =
    document.getElementById(
        "alarm"
    );


    alarmBox.style.display =
    "block";



    if(!alarmPlaying)
    {

        alarmSound.play();

        alarmPlaying = true;

    }


}




function hideAlarm(){


    let alarmBox =
    document.getElementById(
        "alarm"
    );


    alarmBox.style.display =
    "none";


}




function resetAlarm(){


    fetch("/reset_alarm")


    .then(response =>
        response.json()
    )


    .then(data=>{


        console.log(
            data.message
        );



        hideAlarm();



        alarmSound.pause();


        alarmSound.currentTime = 0;


        alarmPlaying=false;


    })


    .catch(error=>{


        console.log(
            "Reset Error:",
            error
        );


    });


}