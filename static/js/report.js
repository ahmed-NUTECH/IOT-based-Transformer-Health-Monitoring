// ==========================================
// REPORT PAGE
// ==========================================

// Current Date
document.getElementById("reportDate").innerHTML =
new Date().toLocaleString();

let tempHistory = [];
let currentHistory = [];

// ==========================================
// Load Sensor Data
// ==========================================

function loadReportData(){

    fetch("/api/sensor-data")

    .then(response => response.json())

    .then(data => {

        // ==================================
        // Live Sensor Values
        // ==================================

        document.getElementById("rTemp").innerHTML =
        data.temperature + " °C";

        document.getElementById("rCurrent").innerHTML =
        data.current + " A";

        document.getElementById("rVoltage").innerHTML =
        data.voltage + " V";

        document.getElementById("rFrequency").innerHTML =
        data.frequency + " Hz";

        document.getElementById("rPF").innerHTML =
        data.power_factor;

        document.getElementById("rSmoke").innerHTML =
        data.smoke;

        // ==================================
        // Summary
        // ==================================

        document.getElementById("ratedVoltage").innerHTML =
        data.voltage + " V";

        document.getElementById("ratedCurrent").innerHTML =
        data.current + " A";

        // ==================================
        // Store History
        // ==================================

        tempHistory.push(Number(data.temperature));
        currentHistory.push(Number(data.current));

        if(tempHistory.length > 20)
            tempHistory.shift();

        if(currentHistory.length > 20)
            currentHistory.shift();

        updateAnalysis();

        updateHealth(data);

        updateCharts();

        updateAlerts(data);

    })

    .catch(error => {

        console.log(error);

    });

}

loadReportData();

setInterval(loadReportData,3000);

// ==========================================
// Average Function
// ==========================================

function average(arr){

    if(arr.length===0)
        return 0;

    return arr.reduce((a,b)=>a+b,0)/arr.length;

}

// ==========================================
// Analysis
// ==========================================

function updateAnalysis(){

    document.getElementById("maxTemp").innerHTML =
    Math.max(...tempHistory).toFixed(1)+" °C";

    document.getElementById("avgTemp").innerHTML =
    average(tempHistory).toFixed(1)+" °C";

    document.getElementById("maxCurrent").innerHTML =
    Math.max(...currentHistory).toFixed(2)+" A";

    document.getElementById("avgCurrent").innerHTML =
    average(currentHistory).toFixed(2)+" A";

}

// ==========================================
// Health Assessment
// ==========================================

function updateHealth(data){

    let health=(data.health || "Healthy").toLowerCase();

    const status=document.getElementById("assessmentStatus");

    const overall=document.getElementById("overallHealth");

    const reason=document.getElementById("assessmentReason");

    const recommendation=document.getElementById("recommendationText");

    reason.innerHTML=
    data.reason || "All monitored parameters are normal.";

    if(Array.isArray(data.recommended_actions))

        recommendation.innerHTML=
        data.recommended_actions.join("<br>");

    else

        recommendation.innerHTML=
        data.recommended_actions || "";



    // ================================
    // HEALTHY
    // ================================

    if(health==="healthy"){

        status.innerHTML="NORMAL";

        overall.innerHTML="NORMAL";

        status.className="normal";

        overall.className="normal";

        document.getElementById("riskPercent").innerHTML="5%";

        document.getElementById("riskLevel").innerHTML="LOW RISK";

        document.getElementById("riskSuggestion").innerHTML=
        data.risk_assessment || "Low Risk";

    }

    // ================================
    // WARNING
    // ================================

    else if(health==="warning"){

        status.innerHTML="WARNING";

        overall.innerHTML="WARNING";

        status.className="warning";

        overall.className="warning";

        document.getElementById("riskPercent").innerHTML="50%";

        document.getElementById("riskLevel").innerHTML="MEDIUM RISK";

        document.getElementById("riskSuggestion").innerHTML=
        data.risk_assessment || "Medium Risk";

    }

    // ================================
    // CRITICAL
    // ================================

    else{

        status.innerHTML="CRITICAL";

        overall.innerHTML="CRITICAL";

        status.className="critical";

        overall.className="critical";

        document.getElementById("riskPercent").innerHTML="90%";

        document.getElementById("riskLevel").innerHTML="HIGH RISK";

        document.getElementById("riskSuggestion").innerHTML=
        data.risk_assessment || "High Risk";

    }

}

// ==========================================
// Temperature Chart
// ==========================================

const tempChart=new Chart(

document.getElementById("temperatureChart"),{

type:"line",

data:{

labels:[],

datasets:[{

label:"Temperature",

data:[],

borderColor:"#EF4444",

fill:false,

tension:0.3

}]

}

});

// ==========================================
// Current Chart
// ==========================================

const currentChart=new Chart(

document.getElementById("currentChart"),{

type:"line",

data:{

labels:[],

datasets:[{

label:"Current",

data:[],

borderColor:"#3EB489",

fill:false,

tension:0.3

}]

}

});

// ==========================================
// Update Charts
// ==========================================

function updateCharts(){

    let labels=[];

    for(let i=0;i<tempHistory.length;i++){

        labels.push(i+1);

    }

    tempChart.data.labels=labels;

    tempChart.data.datasets[0].data=tempHistory;

    tempChart.update();

    currentChart.data.labels=labels;

    currentChart.data.datasets[0].data=currentHistory;

    currentChart.update();

}

// ==========================================
// Alerts
// ==========================================

function updateAlerts(data){

    const table=document.getElementById("alertTable");

    table.innerHTML="";

    let alerts=[];

    if((data.health || "").toLowerCase()=="critical"){

        alerts.push(["Critical Transformer Condition","Critical"]);

    }

    if((data.health || "").toLowerCase()=="warning"){

        alerts.push(["Warning Transformer Condition","Warning"]);

    }

    if(data.smoke=="Warning"){

        alerts.push(["Smoke Detected","Warning"]);

    }

    if(data.smoke=="Critical"){

        alerts.push(["Heavy Smoke Detected","Critical"]);

    }

    alerts.forEach(function(alert){

        const row=document.createElement("tr");

        row.innerHTML=`

        <td>${new Date().toLocaleTimeString()}</td>

        <td>${alert[0]}</td>

        <td>${alert[1]}</td>

        `;

        table.appendChild(row);

    });

}

// ==========================================
// Buttons
// ==========================================

document.addEventListener("DOMContentLoaded",function(){

    const generateBtn=document.getElementById("generateBtn");

    const downloadBtn=document.getElementById("downloadBtn");

    if(generateBtn){

        generateBtn.addEventListener("click",function(){

            fetch("/api/generate-report")

            .then(response=>response.json())

            .then(data=>{

                if(data.status==="success"){

                    alert("Report generated successfully.");

                    loadReportData();

                }

                else{

                    alert(data.message);

                }

            })

            .catch(error=>{

                console.log(error);

                alert("Failed to generate report.");

            });

        });

    }

    if(downloadBtn){

        downloadBtn.addEventListener("click",function(){

            window.location.href="/download-report";

        });

    }

});