document.addEventListener("DOMContentLoaded", () => {
  const socket = io('https://cozmokart.site', {
    transports: ['websocket'],
  });

  function sendAction(msg) {
    socket.send(msg);
  }

  const marker = document.querySelector("#marker");
  const dPad = document.querySelector("#dPad");
  const stopButton = document.querySelector("#stop-button");
  const buttons = {
    "forward": document.querySelector("#forward-button"),
    "backward": document.querySelector("#backward-button"),
    "left": document.querySelector("#left-button"),
    "right": document.querySelector("#right-button"),
    "stop": document.querySelector("#stop-button")
  }
  const msgs = {
    "forward": "s_fwd",
    "backward": "s_bwd",
    "left": "s_lft",
    "right": "s_rht",
    "stop": "stop"
  }

  marker.addEventListener("markerFound", function () {
    console.log("FOUND!!")
    dPad.style.display = "flex";
    stopButton.style.display = "block";
  });

  marker.addEventListener("markerLost", function () {
    dPad.style.display = "none";
    stopButton.style.display = "none";
  });


  Object.keys(buttons).forEach((buttonKey) => {
    console.log(buttonKey)
    buttons[buttonKey].addEventListener("click", () => {
      console.log(buttonKey)
      sendAction(msgs[buttonKey])
    })
  });
});
