let click = false;
document.getElementById("menu-dropdown-btn").addEventListener("click" ,() => {
    click = !click;
    if(click){
        const nav = document.getElementById('nav-sticky');
        const logo = document.getElementById('logo-a');
        const menu = document.getElementById('menu-dropdown-btn');
        nav.style.backgroundColor = 'var(--black-twitter)';
        logo.style.color = 'var(--blue-twitter)';
        menu.style.color = 'var(--extra-extra-light-gray)';
    }
    else{changeNavColor();}

});

document.onscroll = function () {changeNavColor();}
function changeNavColor() {
    const projBackground = document.getElementById('project-background');
    const teamSection = document.getElementById('team-section');
    const nav = document.getElementById('nav-sticky');
    const logo = document.getElementById('logo-a');
    const menu = document.getElementById('menu-dropdown-btn');
    
    if(click){
        return
    }
    if(teamSection.getBoundingClientRect().top <= 0) { // if the distance of the 'specs' section to the browser top is smaller than 0
        nav.style.backgroundColor = 'var(--extra-extra-light-gray)';
        logo.style.color = 'var(--blue-twitter)';
        menu.style.color = 'var(--black-twitter)';
    }
    else if(projBackground.getBoundingClientRect().top <= 0) {
        nav.style.backgroundColor = 'var(--black-twitter)';
        logo.style.color = 'var(--blue-twitter)';
        menu.style.color = 'var(--extra-extra-light-gray)';
    }
    else{
        nav.style.backgroundColor = 'var(--blue-twitter)';
        logo.style.color = 'var(--extra-extra-light-gray)';
        menu.style.color = 'var(--extra-extra-light-gray)';
    }
}