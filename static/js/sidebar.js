document.addEventListener("DOMContentLoaded", function () {

    const menuBtn = document.getElementById("menuBtn");
    const sidebar = document.getElementById("sidebar");
    const mainContent = document.getElementById("mainContent");

    menuBtn.addEventListener("click", function () {

        sidebar.classList.toggle("active");
        mainContent.classList.toggle("shift");

    });

    document.addEventListener("click", function (e) {

        if (
            window.innerWidth <= 768 &&
            !sidebar.contains(e.target) &&
            !menuBtn.contains(e.target)
        ) {

            sidebar.classList.remove("active");
            mainContent.classList.remove("shift");

        }

    });

});