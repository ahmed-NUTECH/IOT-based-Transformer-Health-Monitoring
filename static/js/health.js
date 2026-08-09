// =====================================================
// Transformer Health Status
// =====================================================

function loadHealthStatus() {

    fetch("/api/sensor-data")

    .then(response => response.json())

    .then(data => {

        //--------------------------------------
        // HTML Elements
        //--------------------------------------

        const card = document.getElementById("healthCard");

        const status = document.getElementById("mainHealthStatus");

        const description = document.getElementById("healthDescription");

        const score = document.getElementById("healthScore");

        const recommendation = document.getElementById("recommendation");

        const icon = document.getElementById("healthIcon");

        const conditions = document.getElementById("conditionList");

        const circle = document.querySelector(".score-circle");

        //--------------------------------------
        // Reset Classes
        //--------------------------------------

        card.classList.remove("normal", "warning", "critical");

        document.getElementById("normalBox").className = "status-box";
        document.getElementById("warningBox").className = "status-box";
        document.getElementById("criticalBox").className = "status-box";

        //--------------------------------------
        // Build Active Conditions
        //--------------------------------------

        let list = "";

        if(data.temperature < 60)
            list += "<li> Temperature Normal</li>";
        else if(data.temperature < 80)
            list += "<li> Temperature High</li>";
        else
            list += "<li> Temperature Critical</li>";


        if(data.current < 5)
            list += "<li> Current Normal</li>";
        else if(data.current < 8)
            list += "<li> Current Above Rated</li>";
        else
            list += "<li> Current Overloaded</li>";


        if(data.smoke == "Safe")
            list += "<li>No Smoke Detected</li>";
        else
            list += "<li> Smoke Detected</li>";


        if(data.power_factor >= 0.90)
            list += "<li> Power Factor Normal</li>";
        else
            list += "<li>Low Power Factor</li>";


        conditions.innerHTML = list;

        //--------------------------------------
        // HEALTH STATUS
        //--------------------------------------

        if(data.health == "Healthy"){

            card.classList.add("normal");

            document.getElementById("normalBox").classList.add("active-normal");

            status.innerHTML = "NORMAL";

            description.innerHTML =
            "Transformer is operating safely. All sensor readings are within permissible limits.";

            recommendation.innerHTML =
            "No maintenance required. Continue normal monitoring.";

            score.innerHTML = "100%";

            circle.style.borderColor = "#3EB489";

            icon.setAttribute("data-lucide","shield-check");

        }

        else if(data.health == "Warning"){

            card.classList.add("warning");

            document.getElementById("warningBox").classList.add("active-warning");

            status.innerHTML = "WARNING";

            description.innerHTML =
            "One or more parameters are approaching threshold limits.";

            recommendation.innerHTML =
            "Inspect transformer loading and continue close monitoring.";

            score.innerHTML = "70%";

            circle.style.borderColor = "#F59E0B";

            icon.setAttribute("data-lucide","triangle-alert");

        }

        else{

            card.classList.add("critical");

            document.getElementById("criticalBox").classList.add("active-critical");

            status.innerHTML = "CRITICAL";

            description.innerHTML =
            "Critical operating conditions detected. Immediate action is required.";

            recommendation.innerHTML =
            "Immediately inspect or shut down the transformer to avoid damage.";

            score.innerHTML = "25%";

            circle.style.borderColor = "#EF4444";

            icon.setAttribute("data-lucide","shield-alert");

        }

        //--------------------------------------
        // Refresh Lucide Icons
        //--------------------------------------

        lucide.createIcons();

    })

    .catch(error => {

        console.log(error);

    });

}

// ===========================================
// Load Health History
// ===========================================

function loadHistory() {

    fetch("/api/history")

    .then(response => response.json())

    .then(data => {

        const table = document.getElementById("historyTable");

        table.innerHTML = "";

        data.reverse().forEach(item => {

            let colour = "#3EB489";

            if(item.Status == "Warning")
                colour = "#F59E0B";

            if(item.Status == "Critical")
                colour = "#EF4444";

            table.innerHTML += `

            <tr>

                <td>${item.Time}</td>

                <td style="font-weight:bold;color:${colour};">

                    ${item.Status}

                </td>

            </tr>

            `;

        });

    });

}
