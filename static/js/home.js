document.addEventListener("DOMContentLoaded", () => {
    // Get the hamburger button and side navbar
    const hamburgerBtn = document.getElementById("hamburger-btn");
    const sideNavbar = document.getElementById("side-navbar");

    // Debugging: Check if elements are correctly accessed
    // console.log({ hamburgerBtn, sideNavbar });

    if (!hamburgerBtn || !sideNavbar) {
        console.log("One or more required elements (hamburger-btn, side-navbar) are missing from the DOM.");
        return;
    }

    // Toggle the side navbar visibility on mobile
    hamburgerBtn.addEventListener("click", () => {
        sideNavbar.classList.toggle("open");
    });

    // Close the navbar when a menu item is clicked (optional)
    const menuItems = document.querySelectorAll(".menu-item");
    menuItems.forEach((item) => {
        item.addEventListener("click", () => {
            sideNavbar.classList.remove("open");
        });
    });
});

