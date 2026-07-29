// app.js


function updateStatus() {


    fetch("/status")

    .then(response => response.json())

    .then(data => {


        // Update prediction

        let status =
        document.getElementById("status");


        status.innerHTML =
        data.prediction;



        // Update confidence

        document.getElementById(
            "confidence"
        ).innerHTML =
        data.confidence + "%";



        // Check alarm

        if(data.alarm === true)
        {

            showAlarm();

        }

        else
        {

            hideAlarm();

        }


    })

    .catch(error => {

        console.log(
            "Status Error:",
            error
        );

    });


}



// Update every 2 seconds

setInterval(
    updateStatus,
    2000
);



updateStatus();