document.getElementById("advance-search-button").addEventListener("click", displayAdvance);

function displayAdvance(){
    var advancebtn = document.getElementById("advance-search-button");
    var form_container = document.getElementById("main-form");
    var advance_container = document.getElementById("advance-search-container");
    if(advancebtn.classList.contains('advance-close')){
        advancebtn.textContent = 'Close Avance Search';
        form_container.style.gridTemplateAreas = "'hashtag hashtag''advance advance''advance_container advance_container''go go'";
        advance_container.style.display = 'grid';
        advancebtn.classList.remove("advance-close");

    }
    else{
        advancebtn.textContent = 'Advance Search';
        advance_container.style.display = 'none';
        form_container.style.gridTemplateAreas = "'hashtag hashtag''go go''advance advance'";
        advancebtn.classList.add("advance-close");
    }
}