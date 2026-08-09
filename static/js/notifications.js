// ==========================================
// GLOBAL NOTIFICATION SYSTEM
// ==========================================

document.addEventListener("DOMContentLoaded", function () {

    // ==========================================
    // Alarm Sound
    // ==========================================

    const alarm = new Audio("/static/sounds/alarm.mp3");
    alarm.loop = true;

    let alarmPlaying = false;

    // ==========================================
    // Elements
    // ==========================================

    const bell = document.getElementById("notificationBtn");
    const badge = document.getElementById("notificationBadge");
    const panel = document.getElementById("notificationPanel");
    const notificationList = document.querySelector(".notification-list");

    // ==========================================
    // Bell Click
    // ==========================================

    if (bell && panel) {

        bell.addEventListener("click", function (e) {

            e.stopPropagation();

            panel.style.display =
                panel.style.display === "block" ? "none" : "block";

        });

        document.addEventListener("click", function () {

            panel.style.display = "none";

        });

    }

    // ==========================================
    // Update Notifications
    // ==========================================

    function updateNotifications() {

        const notificationSound =
            localStorage.getItem("notificationSound") || "on";

        // If sound is OFF, stop immediately
        if (notificationSound === "off") {

            alarm.pause();
            alarm.currentTime = 0;
            alarmPlaying = false;

        }

        // ======================================
        // Health Check
        // ======================================

        fetch("/api/sensor-data")

            .then(response => response.json())

            .then(data => {

                if (data.health === "Critical") {

                    if (bell) {

                        bell.classList.add("critical-bell");

                    }

                    if (badge) {

                        badge.style.display = "flex";

                    }

                    if (notificationSound === "on") {

                        if (!alarmPlaying) {

                            alarm.play().catch(() => {});
                            alarmPlaying = true;

                        }

                    } else {

                        alarm.pause();
                        alarm.currentTime = 0;
                        alarmPlaying = false;

                    }

                }

                else {

                    if (bell) {

                        bell.classList.remove("critical-bell");

                    }

                    if (badge) {

                        badge.style.display = "none";

                    }

                    alarm.pause();
                    alarm.currentTime = 0;
                    alarmPlaying = false;

                }

            })

            .catch(error => console.log(error));

        // ======================================
        // Alert Messages
        // ======================================

        fetch("/api/alerts")

            .then(response => response.json())

            .then(alerts => {

                if (!notificationList) return;

                notificationList.innerHTML = "";

                if (alerts.length === 0) {

                    notificationList.innerHTML =
                        "<p>No new notifications</p>";

                    return;

                }

                alerts.forEach(alert => {

                    notificationList.innerHTML += `
                        <div class="notification-item">
                            <strong>${alert.sensor}</strong><br>
                            ${alert.message}
                        </div>
                    `;

                });

            })

            .catch(error => console.log(error));

    }

    // ==========================================
    // Initial Load
    // ==========================================

    updateNotifications();

    // Check every second
    setInterval(updateNotifications, 1000);

});