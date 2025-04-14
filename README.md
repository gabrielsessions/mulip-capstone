# mulip-capstone-neon-carrot

Team Members:
- Christopher Bann
- Douglas Lilly
- Gabriel Sessions
- Jonathan Guzman

Sponsored By: 
- Jivko Sinapov
- Brian Aull
- Emily Carlson

## How to run CozmoKart

### Required Materials
- A charged Cozmo robot
- A Raspberry Pi (or other machine to host the server)
- A laptop with concurrent ethernet, WiFi capabilities, and ROS2 (Ex: Alienware Computer)
- A smartphone with a camera and an updated web browser
- This GitHub repository

### Installations (One-Time Only)
- On the Raspberry Pi/Server machine, install Node.js and npm (LTS). Optionally Python and pip.
  - Install all required packages inside `new-pi-server` by running `npm install`
  - Optional: Install `collision-detection` packages
- On the ROS2 computer install Python3 and pip
  - Install all required Python packages inside `flask-client` by running `pip install -r requirements.txt`

### Setup Steps (Must do every time)
- Boot up the Raspberry Pi/Server
  - Clone this repository and `cd new-pi-server` if it has been updated
  - Run `pm2 run node index.js` (with process manager, recommended) or `node index.js` (w/o process manager)
- Connect the overhead camera to the server (or another computer) and run collision detection script
  - `cd collision-detection`
  - `python3 stuff.py`
  - Optionally disable camera feed display by commenting out some of the last few lines of the script.
- Connect the Alienware to the Cozmo Robot
  - (If needed) Clone down the ROS2 Cozmo repo: https://github.com/solosito/cozmo_ros2_nosdk 
  - Make sure the ethernet cable is plugged in
  - Connect to the Cozmo WiFi network
  - Run `. ~/cozmo_ros2_ws/install/setup.bash` inside the `ros-client` directory
  - Connect the ROS master node to the Cozmo: `ros2 run cozmo_ros2_nosdk bringup`
  - Run the websocket client: `python3 client.py`
- Open up a mobile client
  - Connect to the `Tufts_Secure` network
  - QR Code Interface: http://10.243.89.243/qr.html
  - Simple Controller Interface: http://10.243.89.243/
  - AR Interface: TBD
