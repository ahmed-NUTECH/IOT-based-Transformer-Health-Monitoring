// =====================================================
// DARK MODE
// =====================================================

let darkMode = localStorage.getItem("theme") === "dark";

// =====================================
// APPLY THEME
// =====================================

function applyTheme(){

    if(darkMode){

        document.body.classList.add("dark-mode");

    }

    else{

        document.body.classList.remove("dark-mode");

    }

    // Update Control Panel Button (if available)

    const themeBtn = document.getElementById("themeBtn");

    if(themeBtn){

        themeBtn.innerHTML = darkMode ? "ON" : "OFF";

    }

}

// =====================================
// PAGE LOAD
// =====================================

document.addEventListener("DOMContentLoaded", function(){

    applyTheme();

    // ===============================
    // TOPBAR MOON BUTTON
    // ===============================

    const moonBtn = document.getElementById("darkModeBtn");

    if(moonBtn){

        moonBtn.addEventListener("click", function(){

            darkMode = !darkMode;

            localStorage.setItem(
                "theme",
                darkMode ? "dark" : "light"
            );

            applyTheme();

        });

    }

    // ===============================
    // CONTROL PANEL THEME BUTTON
    // ===============================

    const themeBtn = document.getElementById("themeBtn");

    if(themeBtn){

        themeBtn.addEventListener("click", function(){

            darkMode = !darkMode;

            localStorage.setItem(
                "theme",
                darkMode ? "dark" : "light"
            );

            applyTheme();

        });

    }

});
document.addEventListener("DOMContentLoaded", function () {

    const notificationBtn = document.getElementById("notificationBtn");
    const notificationPanel = document.getElementById("notificationPanel");

    if (notificationBtn && notificationPanel) {

        notificationBtn.addEventListener("click", function (e) {

            e.stopPropagation();

            if (notificationPanel.style.display === "block") {

                notificationPanel.style.display = "none";

            } else {

                notificationPanel.style.display = "block";

            }

        });

        document.addEventListener("click", function () {

            notificationPanel.style.display = "none";

        });

    }

});
// ==========================================
// NAVBAR HEALTH STATUS
// ==========================================

function updateNavbarStatus(){

    fetch("/api/sensor-data")

    .then(response => response.json())

    .then(data => {

        const statusBox = document.getElementById("navbarStatus");
const statusText = document.getElementById("navbarStatusText");


if(!statusBox || !statusText)
    return;


const icon = statusBox.querySelector("i");

        let health = data.health;


        // Remove previous classes

        statusBox.classList.remove(
            "normal",
            "warning",
            "critical"
        );



        if(health === "Healthy"){

            statusText.innerHTML = "Normal";

            statusBox.classList.add("normal");

            icon.setAttribute(
                "data-lucide",
                "shield-check"
            );

        }


        else if(health === "Warning"){

            statusText.innerHTML = "Warning";

            statusBox.classList.add("warning");

            icon.setAttribute(
                "data-lucide",
                "alert-triangle"
            );

        }


        else if(health === "Critical"){

            statusText.innerHTML = "Critical";

            statusBox.classList.add("critical");

            icon.setAttribute(
                "data-lucide",
                "shield-alert"
            );

        }


        // Refresh lucide icons
        lucide.createIcons();


    })


    .catch(error=>{

        console.log(
            "Navbar health error:",
            error
        );

    });

}



// Run every 1 seconds

setInterval(
    updateNavbarStatus,
    1000
);


updateNavbarStatus();