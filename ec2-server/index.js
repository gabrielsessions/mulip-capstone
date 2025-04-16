const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const path = require("path");
const fs = require('fs');
const crypto = require('crypto');
const postgres = require('postgres');
const jwt = require("jsonwebtoken");
require('dotenv').config();

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "*", // Allow all origins (adjust for security)
    methods: ["GET", "POST"]
  }
});

if (!process.env.NEON_CONNECTION) {
  console.error("NEON_CONNECTION environment variables not set")
  process.exit(1);
}

const sql = postgres(process.env.NEON_CONNECTION);

let privateKey;
try {
  privateKey = fs.readFileSync('private-key.pem', 'utf8');
} catch (err) {
  console.error("An error occurred:", err);
  process.exit(1);
}

if (!privateKey) {
  console.error("Fatal Error: No private key");
  process.exit(1);
}


function generateJWT() {
  // Assumes no collisions between UUIDs, add checks if needed
  const uuid = crypto.randomUUID();

  const payload = {
    userID: uuid,
    firstConnection: Date.now()
  }
  const options = {
    expiresIn: '365d', // Token expires in 1 year
    issuer: 'cozmokart'
  };
  const token = jwt.sign(payload, privateKey, options);
  return token;
}

function decodeToken(token, socketID) {
  if (!token)
    return null;

  try {
    const decodedToken = jwt.verify(token, privateKey);
    socketID_JWT.set(socketID, decodedToken.userID);
  }
  catch (err) {
    console.error(err);
    return;
  }
}

async function saveData(socketID, action) {
  const userID = socketID_JWT.get(socketID);
  try {
    const timestamp = await sql`insert into cozmokart (timestamp, user_id, action) values(NOW(), ${userID}, ${action}) returning timestamp;`
  }
  catch (err) {
    console.error(err);
  }
}


=======
async function recordLap(lapNumber) {
  try {
    const timestamp = await sql`insert into cozmokart_laps (timestamp, lap_number) values(NOW(), ${lapNumber}) returning timestamp;`
  }
  catch (err) {
    console.error(err);
  }

}

const socketID_JWT = new Map();

// Serve static files from 'public' directory
app.use(express.static(path.join(__dirname, "public")));

let blockMsgs = false;
io.on("connection", (socket) => {
  console.log(`A user connected: ${socket.id}`);

  socket.on("message", (data) => {
    if (data === "status") {
      io.send("clients: " + socketID_JWT.size);
    }
    if (data.startsWith("token ")) {
      decodeToken(data.split("token ")[1], socket.id);
    }

    // Format: Lap #
    else if (data.startsWith("lap ")) {
      const lapNum = data.split(" ")[1];
      if (parseInt(lapNum))
        recordLap(parseInt(lapNum));
    }

    else if (data === "new connection") {
      const newToken = generateJWT();
      //socketID_JWT.set(socket.id, newToken);
      io.send(newToken);
    }

    else if (data === "stop_up" && !blockMsgs) {
      blockMsgs = true;
      setTimeout(() => {
        blockMsgs = false;
      }, 500);
      io.emit("message", "X:0, Y:0")
      console.log("STOP -- COLLISION")
    }
    
    else if (data && !blockMsgs) {
      if (socketID_JWT.has(socket.id)) {
        saveData(socket.id, data);
      }
      console.log(`Message from ${socket.id}:`, data);
      io.emit("message", data); // Broadcast to all clients
    }
  });

  socket.on("disconnect", () => {
    if (socketID_JWT.has(socket.id)) {
      socketID_JWT.delete(socket.id);
    }
    console.log(`User disconnected: ${socket.id}`);
  });
});

const PORT = 3000;
server.listen(PORT, () => {
  console.log(`Socket.IO server running on port ${PORT}`);
});
