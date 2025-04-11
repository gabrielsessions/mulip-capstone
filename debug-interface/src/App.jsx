import { useEffect, useState } from 'react'
import WebSocketLog from './components/WebSocketLog';
import { io } from 'socket.io-client';

function App() {

  const [WS, setWS] = useState(null);
  const [messages, setMessages] = useState([]);
  const [popup, setPopup] = useState({
    visible: false,
    message: "Alert!"
  })

  const showAlert = message => {
    setPopup({
      visible: true,
      message: message
    })
    setTimeout(() => {
      setPopup({
        visible: false,
        message: ""
      })
    }, 3000);
  }


  useEffect(() => {
    const initialConnect = () => {
      console.log("Socket connection attempted:");

      // Establish the Socket.IO connection
      const socket = io('/', {
        transports: ['websocket'],
      });

      socket.on("connect", () => {
        console.log("Connected to server!");
        setWS(socket); // Save the socket to state after a successful connection
        //socket.emit("message", "Hello!"); // Emit a message to the server
      });

      socket.on("disconnect", () => {
        console.log("Disconnected from server!");
        setWS(null);
        showAlert("Socket connection closed. Please reload the page to reconnect!");
      });

      socket.on("message", (message) => {
        console.log("Received from server:", message);
        setMessages((prev) => [...prev, message]);
      });

      socket.on("error", (err) => {
        console.error("Socket error:", err);
      });
    };

    initialConnect();
  }, []);


  return (
    <>

      <div className="flex justify-center items-center min-h-screen bg-gray-200">
        <div className="absolute top-2 right-2">
          {
            popup.visible ?
              <div className="w-full px-4 py-3 text-sm border rounded border-blue-100 bg-blue-50 text-blue-500" role="alert">
                <p>{popup.message}</p>
              </div>
              :
              <></>
          }
        </div>
        <WebSocketLog connected={WS !== undefined && WS !== null} log={messages} sendMessage={(message) => WS.send(message)} disconnect={() => {
          WS.close();
        }} />
      </div>

    </>

  )
}

export default App;
