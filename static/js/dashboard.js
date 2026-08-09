// ======================================================
// IoT Transformer Monitoring System
// Dashboard JavaScript
// ======================================================

let labels = [];
let temperatureData = [];
let currentData = [];


// ======================================================
// CHECK ELEMENT
// ======================================================

function getElement(id) {
    return document.getElementById(id);
}


// ======================================================
// TEMPERATURE CHART
// ======================================================

const temperatureCanvas = getElement("temperatureChart");

let temperatureChart = null;

if (temperatureCanvas) {

    temperatureChart = new Chart(
        temperatureCanvas,
        {
            type: "line",

            data: {
                labels: labels,

                datasets: [{
                    label: "Temperature (°C)",

                    data: temperatureData,

                    borderColor: "#EF4444",

                    backgroundColor:
                        "rgba(239,68,68,0.15)",

                    fill: true,

                    tension: 0.4
                }]
            },

            options: {
                responsive: true,

                maintainAspectRatio: false,

                animation: false,

                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        }
    );
}


// ======================================================
// CURRENT CHART
// ======================================================

const currentCanvas = getElement("currentChart");

let currentChart = null;

if (currentCanvas) {

    currentChart = new Chart(
        currentCanvas,
        {
            type: "line",

            data: {
                labels: labels,

                datasets: [{
                    label: "Current (A)",

                    data: currentData,

                    borderColor: "#3B82F6",

                    backgroundColor:
                        "rgba(59,130,246,0.15)",

                    fill: true,

                    tension: 0.4
                }]
            },

            options: {
                responsive: true,

                maintainAspectRatio: false,

                animation: false,

                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        }
    );
}


// ======================================================
// UPDATE VALUE
// ======================================================

function updateValue(id, value) {

    const element = getElement(id);

    if (!element) return;

    element.innerHTML = value;
}


// ======================================================
// HEALTH COLOUR
// ======================================================

function updateHealthAppearance(status) {

    const element = getElement("healthStatus");

    if (!element) return;

    element.classList.remove(
        "normal",
        "warning",
        "critical"
    );

    if (status === "Healthy") {

        element.classList.add("normal");

    }

    else if (status === "Warning") {

        element.classList.add("warning");

    }

    else if (status === "Critical") {

        element.classList.add("critical");

    }

}


// ======================================================
// UPDATE SENSOR CARDS
// ======================================================

function updateCardColour(
    id,
    value,
    warning,
    critical
) {

    const element = getElement(id);

    if (!element) return;

    const card =
        element.closest(".sensor-card");

    if (!card) return;

    card.classList.remove(
        "normal-card",
        "warning-card",
        "critical-card"
    );

    value = Number(value);

    if (value >= critical) {

        card.classList.add(
            "critical-card"
        );

    }

    else if (value >= warning) {

        card.classList.add(
            "warning-card"
        );

    }

    else {

        card.classList.add(
            "normal-card"
        );

    }

}


// ======================================================
// LOAD SENSOR DATA
// ======================================================

function loadSensorData() {

    fetch(
        "/api/sensor-data?t=" + Date.now(),
        {
            method: "GET",

            cache: "no-store"
        }
    )

    .then(response => {

        if (!response.ok) {

            throw new Error(
                "API Error: " +
                response.status
            );

        }

        return response.json();

    })

    .then(data => {

        console.log(
            "========== LIVE SENSOR DATA =========="
        );

        console.log(data);


        // ==================================================
        // API ERROR
        // ==================================================

        if (data.status === "error") {

            console.error(
                data.message
            );

            return;
        }


        // ==================================================
        // VOLTAGE
        // ==================================================

        updateValue(
            "voltageValue",
            `${data.voltage ?? "--"} V`
        );


        // ==================================================
        // CURRENT
        // ==================================================

        updateValue(
            "currentValue",
            `${data.current ?? "--"} A`
        );


        // ==================================================
        // TEMPERATURE
        // ==================================================

        updateValue(
            "temperatureValue",
            `${data.temperature ?? "--"} °C`
        );


        // ==================================================
        // FREQUENCY
        // ==================================================

        updateValue(
            "frequencyValue",
            `${data.frequency ?? "--"} Hz`
        );


        // ==================================================
        // POWER FACTOR
        // ==================================================

        updateValue(
            "powerFactor",
            data.power_factor ?? "--"
        );


        // ==================================================
        // SMOKE
        // ==================================================

        updateValue(
            "smokeStatus",
            data.smoke ?? "--"
        );


        // ==================================================
        // SMOKE MESSAGE
        // ==================================================

        const smokeMessage =
            getElement("smokeMessage");

        if (smokeMessage) {

            if (
                String(data.smoke)
                    .toLowerCase() === "safe"
            ) {

                smokeMessage.innerHTML =
                    "No Smoke Detected";

            }

            else {

                smokeMessage.innerHTML =
                    "Smoke Detected";

            }

        }


        // ==================================================
        // HEALTH
        // ==================================================

        updateValue(
            "healthStatus",
            data.health ?? "Unknown"
        );

        updateHealthAppearance(
            data.health
        );


        // ==================================================
        // TRANSFORMER TYPE
        // ==================================================

        const transformerType =
            getElement("transformerType");

        if (
            transformerType &&
            data.transformer_type
        ) {

            transformerType.value =
                data.transformer_type;

        }


        // ==================================================
        // RATED CURRENT
        // ==================================================

        const ratedCurrent =
            getElement("ratedCurrent");

        if (
            ratedCurrent &&
            data.rated_current !== undefined
        ) {

            let ratedValue =
                Number(data.rated_current);

            // Find matching option
            for (
                let option
                of ratedCurrent.options
            ) {

                let optionValue =
                    parseFloat(option.value);

                let optionText =
                    parseFloat(option.text);

                if (
                    optionValue === ratedValue ||
                    optionText === ratedValue
                ) {

                    ratedCurrent.value =
                        option.value;

                    break;

                }

            }

        }


        // ==================================================
        // TEMPERATURE CARD
        // ==================================================

        updateCardColour(
            "temperatureValue",
            Number(data.temperature),
            60,
            80
        );


        // ==================================================
        // CURRENT CARD
        // ==================================================

        const rated =
            Number(
                data.rated_current || 5
            );

        updateCardColour(
            "currentValue",
            Number(data.current),
            rated,
            rated * 1.2
        );


        // ==================================================
        // LIVE CHART DATA
        // ==================================================

        const currentTime =
            new Date().toLocaleTimeString();


        labels.push(currentTime);

        temperatureData.push(
            Number(data.temperature)
        );

        currentData.push(
            Number(data.current)
        );


        // Keep last 15 readings

        if (labels.length > 15) {

            labels.shift();

            temperatureData.shift();

            currentData.shift();

        }


        // ==================================================
        // UPDATE CHARTS
        // ==================================================

        if (temperatureChart) {

            temperatureChart.update();

        }

        if (currentChart) {

            currentChart.update();

        }


        // ==================================================
        // DEBUG
        // ==================================================

        console.log(
            "Temperature:",
            data.temperature
        );

        console.log(
            "Current:",
            data.current
        );

        console.log(
            "Voltage:",
            data.voltage
        );

        console.log(
            "Frequency:",
            data.frequency
        );

        console.log(
            "Power Factor:",
            data.power_factor
        );

        console.log(
            "Smoke:",
            data.smoke
        );

        console.log(
            "Health:",
            data.health
        );

        console.log(
            "Reason:",
            data.reason
        );

        console.log(
            "Risk:",
            data.risk_assessment
        );

    })

    .catch(error => {

        console.error(
            "Dashboard Sensor Error:",
            error
        );

    });

}


// ======================================================
// START DASHBOARD
// ======================================================

loadSensorData();


// ======================================================
// REFRESH EVERY 2 SECONDS
// ======================================================

setInterval(
    loadSensorData,
    2000
);