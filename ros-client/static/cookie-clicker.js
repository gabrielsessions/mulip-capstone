import { io } from "./socket.io.esm.min.js"

let localCookieCount = 0;
let globalCookieCount = 0;
const socket = io(); // Declare socket globally

const commands = ["f_fwd","s_fwd","f_bwd", "s_bwd", "f_lft", "s_lft", "f_rht", "s_rht", "stop"]

function cookieClicked() {
  localCookieCount++;
  document.getElementById("local-score").innerText = localCookieCount;

  const curPos = document.getElementById("cookie").getAttribute("position");
  console.log(curPos)

  // Change cookie position
  const xPos = Math.floor(Math.random() * 5) ;
  const yPos = Math.floor(Math.random() * 5) ;
  const zPos = Math.floor(Math.random() * 5) ;
  //const newCoords = `${xPos} ${yPos} ${zPos}`;
  const newCoords = {
    x: curPos.x + Math.random()*2 - 1,
    y: curPos.y + Math.random()*2 - 1,
    z: curPos.z
  }

  console.log(newCoords)

  document.getElementById("cookie").setAttribute("position", newCoords);

  socket.send(commands[Math.floor(Math.random() * commands.length)]); // Update global score
}

function globalScoreUpdate(newVal) {
  if (!(newVal instanceof Number)) {
    newVal = parseInt(newVal);
  }
  globalCookieCount = newVal;
  document.getElementById("global-score").innerText = globalCookieCount;
}

window.onload = () => {
  console.log("Loading DOM");
  const cookie = document.querySelector('#cookie');

  cookie.addEventListener('click', () => {
    cookieClicked();
    console.log("Local Count:", localCookieCount);
  });

  socket.on("response", (data) => {
    console.log("Message from server:", data);
    globalScoreUpdate(data)
  });

  socket.on("serverReply", (data) => {
    console.log("Reply from server:", data);
  });

  socket.on("connect", () => {
    console.log("Socket ID: ", socket.id);
  });

};
