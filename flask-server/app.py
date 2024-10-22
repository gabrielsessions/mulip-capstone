from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__, template_folder='templates', static_folder='static')
socketio = SocketIO(app, cors_allowed_origins="*", supports_credentials=True)

CORS(app, supports_credentials=True)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    print('Received message: ' + msg)
    emit('response', 'Server received: ' + msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
