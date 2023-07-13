// console.log("start");
document.getElementById("menu-dropdown-btn").addEventListener("click", displayMenu);


function displayMenu() {
    // console.log("click");
    var menubtn = document.getElementById("menu-dropdown-btn");
    if(menubtn.classList.contains('close')){
        // document.getElementById("menu-dropdown").style.opacity = '0';
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
            openDropdown.classList.remove('show');
            }
        }
        menubtn.classList.remove("close");
        menubtn.classList.toggle("open");
    }
    else{
        document.getElementById("menu-dropdown").classList.toggle("show");
        // document.getElementById("menu-dropdown").style.opacity = '1';
        menubtn.classList.toggle("close");
        menubtn.classList.remove("open");
    }
    

}

var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
    if(document.getElementById("menu-dropdown-btn").classList.contains('close')){
        return
    }
    var currentScrollPos = window.pageYOffset;
    if (prevScrollpos > currentScrollPos) {
        document.getElementById("nav-sticky").style.top = "0";
    } else {
        document.getElementById("nav-sticky").style.top = "-100px";
    }
    prevScrollpos = currentScrollPos;
}