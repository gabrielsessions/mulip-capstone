from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/cozmo_ros2_ws/src/cozmo_ros2_nosdk/cozmo_ros2_nosdk/')))

from teleop_twist_web_prime import TeleopTwistWeb, JoystickTeleop

app = Flask(__name__, template_folder='templates', static_folder='static')
socketio = SocketIO(app, cors_allowed_origins="*", supports_credentials=True)

CORS(app, supports_credentials=True)

cozmoCtrl = JoystickTeleop()


@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/debug')
def debug():
    return render_template('debug.html')

@app.route('/teleop-demo')
def teleop_demo():
    return render_template('teleop-demo.html')
    

@socketio.on('message')
def handle_message(msg):
    action = str(msg)
    cozmoCtrl.send_command(action)
    #emit(app, action)
    

@socketio.on('connect')
def send_global_score():
    print("Connection!")

port_number = 8080
if __name__ == '__main__':
    socketio.run(app, port=port_number)
