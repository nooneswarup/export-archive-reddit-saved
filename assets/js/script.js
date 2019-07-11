function idnum()    {
    var wrappers = document.getElementsByClassName('mdwrapper');
    for (var i = 0; i < wrappers.length; i++) {
        console.log(wrappers[i].id);
}}

function toggles(n) {
  var x = document.getElementById(n);
   if(x == null){
    console.log("it is null");
  }
  else if (x.style.display === "block") {
    x.style.display = "none";
  } else {
    x.style.display = "block";
  }
}

function filterlist() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    ul = document.getElementById("filterlist");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}
