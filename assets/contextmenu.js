var elements = document.getElementsByClassName("song")
for (let element of elements) {
  element.addEventListener("contextmenu", function(event){
    event.preventDefault();
    playelement(element);
  });
  function playelement(element) {
    if (!(document.getElementById(element.id+"player") == null)) {
      preserve = document.getElementById(element.id+"player").playing;
    }
    else {
      preserve = false
    }
    for (let song of document.getElementsByTagName("audio")) {
      song.pause()
      song.playing = false;
    }
    if (!(document.getElementById(element.id+"player") == null)) {
      document.getElementById(element.id+"player").playing = preserve;
    }
    if (document.getElementById(element.id+"player") == null) {
      audioelement = new Audio("/songs/get?song="+element.id+"&library="+document.getElementById("library").innerText);
      audioelement.id = element.id + "player";
      audioelement.volume = 0.1;
      element.append(audioelement);
      audioelement.play();
      console.log("playing song "+element.id);
      audioelement.playing = true;
    }
    else {
      audioelement = document.getElementById(element.id+"player")
      if (!audioelement.playing) {
        audioelement.play();
        audioelement.playing = true;
        console.log("playing song "+element.id);
      }
      else {
        audioelement.pause();
        audioelement.playing = false;
        console.log("pausing song "+element.id);
      }
    }
  }
};