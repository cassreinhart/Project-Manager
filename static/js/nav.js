const dropDown = document.getElementById("dropdown-menu-icon");
const navList = document.getElementById("navbar-list");

document.addEventListener("DOMContentLoaded", function() {
    dropDown.addEventListener("click", function () {
        console.log("click");
        // console.log(navList.classList)
        console.log(navList)
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
