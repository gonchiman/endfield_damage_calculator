const button = document.getElementById("menu-toggle");
const sidebar = document.getElementById("sidebar");

button.addEventListener("click", function (event) {
    event.stopPropagation();
    sidebar.classList.toggle("closed");
});

sidebar.addEventListener("click", function (event) {
    event.stopPropagation();
});

document.addEventListener("click", function () {
    if (!sidebar.classList.contains("closed")) {
        sidebar.classList.add("closed");
    }
});