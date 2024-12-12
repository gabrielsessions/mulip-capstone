import os, socketio, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/cozmo_ros2_ws/src/cozmo_ros2_nosdk/cozmo_ros2_nosdk/')))

from teleop_twist_web_prime import TeleopTwistWeb

# Create a Socket.IO client
sio = socketio.Client()
cozmoCtrl = TeleopTwistWeb()

# Define event handler for the connection
@sio.event
def connect():
    print("Connected to the server")

# Define event handler for receiving messages
@sio.event
def message(data):
    print("Received message:", data)
    action = str(data)
    cozmoCtrl.send_command(action)

# Define event handler for disconnection
@sio.event
def disconnect():
    print("Disconnected from the server")

# Connect to the Socket.IO server (replace with your server URL)
server_url = "https://mulip-flask-server-131677620155.us-east4.run.app" 
sio.connect(server_url)

# Keep the program running to listen for messages
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Connection closed")
    sio.disconnect()
