import { io } from "./socket.io.esm.min.js"

const socket = io(); // Declare socket globally

const commands = ["f_fwd","s_fwd","f_bwd", "s_bwd", "f_lft", "s_lft", "f_rht", "s_rht", "stop"]


function globalScoreUpdate(newVal) {
  document.getElementById("current-action").innerText = newVal;
}

const buttons = ["s_fwd", "s_bwd", "s_lft", "s_rht", "stop"];

window.onload = () => {
  console.log("Loading DOM");

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

  buttons.forEach(id => {
    document.getElementById(id).addEventListener('click', () => {
        console.log("Button clicked: ", id);
        socket.send(id);
    })
  });

};
