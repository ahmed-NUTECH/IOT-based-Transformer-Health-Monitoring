// =====================================================
// IoT-Based Distribution Transformer
// Control Panel
// =====================================================

document.addEventListener("DOMContentLoaded", function () {

    // =====================================================
    // VARIABLES
    // =====================================================

    let autoRefresh =
        localStorage.getItem("autoRefresh") !== "off";

    // =====================================================
    // REFRESH SENSOR DATA
    // =====================================================

    const refreshBtn = document.getElementById("refreshBtn");

    if (refreshBtn) {

        refreshBtn.addEventListener("click", function () {

            fetch("/api/sensor-data")
                .then(response => response.json())
                .then(data => {

                    alert("✅ Sensor data refreshed successfully.");

                })
                .catch(error => {

                    alert("❌ Unable to refresh sensor data.");

                });

        });

    }

    // =====================================================
    // RESET ALERTS
    // =====================================================

    const resetBtn = document.getElementById("resetBtn");

    if (resetBtn) {

        resetBtn.addEventListener("click", function () {

            if (confirm("Clear all active alerts?")) {

                alert("✅ Alerts reset successfully.");

            }

        });

    }

    // =====================================================
    // EXPORT CSV
    // =====================================================

    const exportBtn = document.getElementById("exportBtn");

    if (exportBtn) {

        exportBtn.addEventListener("click", function () {

            window.location.href = "/api/export-csv";

        });

    }

    // =====================================================
    // DARK MODE
    // =====================================================

    const themeBtn = document.getElementById("themeBtn");

    if (themeBtn) {

        const darkMode =
            localStorage.getItem("theme") === "dark";

        themeBtn.innerHTML = darkMode ? "ON" : "OFF";

        themeBtn.addEventListener("click", function () {

            document.body.classList.toggle("dark-mode");

            if (document.body.classList.contains("dark-mode")) {

                localStorage.setItem("theme", "dark");
                themeBtn.innerHTML = "ON";

            }

            else {

                localStorage.setItem("theme", "light");
                themeBtn.innerHTML = "OFF";

            }

        });

    }

    // =====================================================
    // NOTIFICATION SOUND
    // =====================================================

    const soundBtn = document.getElementById("soundBtn");

    if (soundBtn) {

        let notificationSound =
            localStorage.getItem("notificationSound") || "on";

        soundBtn.innerHTML =
            notificationSound === "on" ? "ON" : "OFF";

        soundBtn.addEventListener("click", function () {

            if (notificationSound === "on") {

                notificationSound = "off";

                localStorage.setItem(
                    "notificationSound",
                    "off"
                );

                soundBtn.innerHTML = "OFF";
                

            }

            else {

                notificationSound = "on";

                localStorage.setItem(
                    "notificationSound",
                    "on"
                );

                soundBtn.innerHTML = "ON";

            }

        });

    }

    // =====================================================
    // AUTO REFRESH
    // =====================================================

    const autoBtn = document.getElementById("autoBtn");

    if (autoBtn) {

        autoBtn.innerHTML =
            autoRefresh ? "ON" : "OFF";

        autoBtn.addEventListener("click", function () {

            autoRefresh = !autoRefresh;

            if (autoRefresh) {

                autoBtn.innerHTML = "ON";

                localStorage.setItem(
                    "autoRefresh",
                    "on"
                );

            }

            else {

                autoBtn.innerHTML = "OFF";

                localStorage.setItem(
                    "autoRefresh",
                    "off"
                );

            }

        });

    }

    // =====================================================
    // AUTO REFRESH TIMER
    // =====================================================

    setInterval(function () {

        if (!autoRefresh) return;

        fetch("/api/sensor-data")
            .catch(error => console.log(error));

    }, 5000);

});