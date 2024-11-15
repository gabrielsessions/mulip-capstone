from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
socketio = SocketIO(app, cors_allowed_origins="*", supports_credentials=True)

CORS(app, supports_credentials=True)

cookieClickerScore = 0

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    global cookieClickerScore
    print('Received cookie click!', cookieClickerScore)
    cookieClickerScore += 1
    emit('response', str(cookieClickerScore), broadcast=True)

@socketio.on('connect')
def send_global_score():
    print("Connection!")
    emit('response', cookieClickerScore)

port_number = os.environ["PORT"] if "PORT" in os.environ else 8080
if __name__ == '__main__':
    socketio.run(app, port=port_number)
