/**
 * Created by Z on 20/03/2017.
 */
function openGenre(evt, genre) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("genretabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("genretablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(genre).style.display = "block";
    evt.currentTarget.className += " active";
}