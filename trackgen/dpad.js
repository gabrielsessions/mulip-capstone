const socket = io('/', {
  transports: ['websocket'],
});

function sendAction(msg) {
  socket.send(msg);
}

const marker = document.querySelector("#marker");
const dPad = document.querySelector("#dPad");
const stopButton = document.querySelector("#stopButton");
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
  dPad.style.display = "flex";
  stopButton.style.display = "block";
});

marker.addEventListener("markerLost", function () {
  dPad.style.display = "none";
  stopButton.style.display = "none";
});

Object.keys(buttons).forEach((buttonKey) => {
  console.log(buttons, buttonKey)
  buttons[buttonKey].addEventListener("click", () => {
    sendAction(msgs[buttonKey])
  })
})
