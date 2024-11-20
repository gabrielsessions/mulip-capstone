from flask import Flask, request, jsonify, send_file, render_template, url_for
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from io import BytesIO
import os
import jwt
import uuid
import datetime
import qrcode

# Load RSA keys for JWT signing and verification
with open("private_key.pem", "r") as f:
    PRIVATE_KEY = f.read()

with open("public_key.pem", "r") as f:
    PUBLIC_KEY = f.read()


user_counter = 1

def create_jwt(user_id):
    """
    Generates a JWT with a 1-hour expiration.
    """
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {
        "iss": "myapp",
        "sub": user_id,
        "exp": expiration_time,
        "jti": str(uuid.uuid4())
    }
    token = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
    return token


app = Flask(__name__, template_folder='templates', static_folder='static')
socketio = SocketIO(app, cors_allowed_origins="*", supports_credentials=True)

CORS(app, supports_credentials=True)

cookieClickerScore = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/qr')
def qr():
    return render_template('qr.html')

@app.route("/generate_qr", methods=["POST"])
def generate_qr():
    """
    Generates a QR code with a URL pointing to the landing page.
    """
    landing_url = f"http://127.0.0.1:8080/cookie"
    print(landing_url)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(landing_url)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    img_io = BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)
    
    return send_file(img_io, mimetype="image/png")

@app.route("/cookie")
def landing():
    """
    Generates a JWT for the user upon loading the landing page and embeds it in the template.
    """
    # global user_counter  
    # user_id = f"user{user_counter}"  
    # user_counter += 1  
    # token = create_jwt(user_id)
    
    return render_template("cookie.html")


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

port_number = 8080
if __name__ == '__main__':
    socketio.run(app, port=port_number)
