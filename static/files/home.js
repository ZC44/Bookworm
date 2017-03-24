/**
 * Created by Z on 20/03/2017.
 */
function openHomeTabs(evt, tab) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("hometabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("hometablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tab).style.display = "block";
    evt.currentTarget.className += " active";
}
// Default Open popular books
document.getElementById("pop").click();