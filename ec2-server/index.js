const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const path = require("path");

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "*", // Allow all origins (adjust for security)
    methods: ["GET", "POST"]
  }
});

// Serve static files from 'public' directory
app.use(express.static(path.join(__dirname, "public")));

io.on("connection", (socket) => {
  console.log(`A user connected: ${socket.id}`);
  
  socket.on("message", (data) => {
    console.log(`Message from ${socket.id}:`, data);
    io.emit("message", data); // Broadcast to all clients
  });

  socket.on("disconnect", () => {
    console.log(`User disconnected: ${socket.id}`);
  });
});

const PORT = 3000;
server.listen(PORT, () => {
  console.log(`Socket.IO server running on port ${PORT}`);
});
