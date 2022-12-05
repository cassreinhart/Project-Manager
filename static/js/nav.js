const dropDown = document.getElementById("dropdown-menu-icon");
const navList = document.getElementsByClassName("navbar-list");

document.addEventListener("DOMContentLoaded", function(evt) {
    dropDown.addEventListener("click", function (evt) {
        console.log("click");
        navList.classList.toggle("active");
        // if (navList.classList.includes("active")) {
        //     navList.classList.remove("active");    
        //     console.log("inactive");
        // }
        // else {
        //     navList.classList.add("active");
        //     console.log("inactive");
        // }
    });
});
