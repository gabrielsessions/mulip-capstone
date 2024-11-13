import jwt
import uuid
import datetime
import qrcode
import base64
from flask import Flask, request, jsonify, send_file, render_template
from cryptography.fernet import Fernet
from io import BytesIO
import hashlib
from urllib.parse import quote as url_quote


app = Flask(__name__)

# Load RSA keys
with open("private_key.pem", "r") as f:
    PRIVATE_KEY = f.read()

with open("public_key.pem", "r") as f:
    PUBLIC_KEY = f.read()

# Symmetric key for encrypting QR code data
ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

# In-memory store for single-use tokens and refresh tokens
used_tokens = set()
refresh_tokens = {}

def create_jwt(user_id, audience="myapp.com"):
    session_id = str(uuid.uuid4())
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    
    payload = {
        "iss": "myapp",
        "aud": audience,
        "sub": user_id,
        "session_id": session_id,
        "exp": expiration_time,
        "jti": str(uuid.uuid4())
    }
    
    token = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
    return token

def generate_device_fingerprint(user_agent, ip_address):
    fingerprint_source = f"{user_agent}-{ip_address}"
    fingerprint = hashlib.sha256(fingerprint_source.encode()).hexdigest()
    return fingerprint

def generate_qr_code(jwt_token):
    encrypted_token = cipher_suite.encrypt(jwt_token.encode())
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(base64.urlsafe_b64encode(encrypted_token).decode())
    qr.make(fit=True)
    
    img = qr.make_image(fill="black", back_color="white")
    return img

@app.route("/")
def index():
    return render_template("index.html")  # Ensure 'index.html' is in your 'templates' folder

@app.route("/generate_qr", methods=["POST"])
def generate_qr():
    data = request.json
    user_id = data.get("user_id")
    
    if not user_id:
        return jsonify({"error": "User ID required"}), 400
    
    token = create_jwt(user_id)
    img = generate_qr_code(token)
    
    img_io = BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)
    
    return send_file(img_io, mimetype="image/png")

@app.route("/verify_qr", methods=["POST"])
def verify_qr():
    data = request.json
    encrypted_token = data.get("token")
    user_agent = data.get("user_agent")
    ip_address = request.remote_addr
    
    try:
        decoded_token = cipher_suite.decrypt(base64.urlsafe_b64decode(encrypted_token)).decode()
        payload = jwt.decode(decoded_token, PUBLIC_KEY, algorithms=["RS256"])
        
        jti = payload.get("jti")
        if jti in used_tokens:
            return jsonify({"error": "Token already used"}), 400
        
        used_tokens.add(jti)
        device_fingerprint = generate_device_fingerprint(user_agent, ip_address)
        return jsonify({"status": "valid", "user_id": payload["sub"], "device_fingerprint": device_fingerprint}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Session expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 400

if __name__ == "__main__":
    app.run(debug=True)
