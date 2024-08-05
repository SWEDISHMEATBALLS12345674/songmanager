var wage = document.getElementById("query");
  wage.addEventListener("keydown", function (e) {
    if (e.keyCode === 13) {
        validate(e);
    }
  });

  function validate(e) {
    window.location.replace("search?search="+document.getElementById("query").value);
  }

  function addToServer(id) {
    window.location.replace("https://yt.liraaa.com/getaudio.php?v="+id+"&playlist="+document.getElementById(id).value);
  }