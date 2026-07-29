// history.js



function loadHistory(){


    fetch("/history")


    .then(response =>
        response.json()
    )


    .then(data=>{


        let table =
        document.getElementById(
            "history"
        );



        table.innerHTML = "";



        // Latest event first

        data.reverse();



        data.forEach(event=>{


            table.innerHTML += `

            <tr>

            <td>
            ${event.Time}
            </td>


            <td>
            ${event.Confidence}%
            </td>


            <td>
            ${event.Status}
            </td>


            </tr>

            `;


        });



    })


    .catch(error=>{


        console.log(
            "History Error:",
            error
        );


    });


}



// Refresh history every 5 seconds

setInterval(
    loadHistory,
    5000
);



loadHistory();