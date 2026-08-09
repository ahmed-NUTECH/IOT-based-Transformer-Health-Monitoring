// =====================================================
// LOAD ALERTS
// =====================================================

function loadAlerts(){

    fetch("/api/alerts")

    .then(response => response.json())

    .then(data =>{

        const container = document.getElementById("alertContainer");
        const table = document.getElementById("alertTable");

        container.innerHTML = "";
        table.innerHTML = "";

        let total = data.length;
        let warning = 0;
        let critical = 0;

        if(total === 0){

            container.innerHTML = `

            <div class="no-alert">

                <i data-lucide="shield-check"></i>

                <h3>No Active Alerts</h3>

                <p>Transformer is operating normally.</p>

            </div>

            `;

            document.getElementById("systemStatus").innerHTML="Normal";

        }

        data.forEach(alert=>{

            if(alert.severity=="Warning")
                warning++;

            if(alert.severity=="Critical")
                critical++;

            container.innerHTML += `

            <div class="alert-item ${alert.severity.toLowerCase()}">

                <h3>${alert.sensor}</h3>

                <p>${alert.message}</p>

                <strong>${alert.value}</strong>

            </div>

            `;

            table.innerHTML += `

            <tr>

                <td>${alert.sensor}</td>

                <td>${alert.value}</td>

                <td>

                    <span class="badge ${alert.severity.toLowerCase()}">

                        ${alert.severity}

                    </span>

                </td>

                <td>${alert.message}</td>

            </tr>

            `;

        });

        document.getElementById("totalAlerts").innerHTML=total;
        document.getElementById("criticalAlerts").innerHTML=critical;
        document.getElementById("warningAlerts").innerHTML=warning;

        if(critical>0)
            document.getElementById("systemStatus").innerHTML="Critical";
        else if(warning>0)
            document.getElementById("systemStatus").innerHTML="Warning";
        else
            document.getElementById("systemStatus").innerHTML="Normal";

        lucide.createIcons();

    })

    .catch(error=>{

        console.log(error);

    });

}
function updateSystemStatus(){


fetch("/api/sensor-data")

.then(response=>response.json())

.then(data=>{


let status =
document.getElementById("systemStatus");


if(!status)
return;



status.innerHTML=data.health;



status.className="";



if(data.health=="Healthy"){

    status.classList.add("normal");

}


else if(data.health=="Warning"){

    status.classList.add("warning");

}


else if(data.health=="Critical"){

    status.classList.add("critical");

}



});


}


setInterval(
updateSystemStatus,
2000
);


updateSystemStatus();