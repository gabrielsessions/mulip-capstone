from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os
from teleop_twist_web_prime import TeleopTwistWeb

app = Flask(__name__, template_folder='templates', static_folder='static')
socketio = SocketIO(app, cors_allowed_origins="*", supports_credentials=True)

CORS(app, supports_credentials=True)

cozmoCtrl = TeleopTwistWeb()

cookieClickerScore = 0

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/debug')
def debug():
    return render_template('debug.html')
    

@socketio.on('message')
def handle_message(msg):
    '''global cookieClickerScore
    print('Received cookie click!', cookieClickerScore)
    cookieClickerScore += 1
    emit('response', str(cookieClickerScore), broadcast=True)'''
    print(msg) 
    cozmoCtrl.send_command(msg)
    

@socketio.on('connect')
def send_global_score():
    print("Connection!")
    emit('response', cookieClickerScore)

port_number = 8080
if __name__ == '__main__':
    socketio.run(app, port=port_number)
