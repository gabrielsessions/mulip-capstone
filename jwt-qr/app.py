import jwt
import uuid
import datetime
import qrcode
from flask import Flask, request, jsonify, send_file, render_template, redirect
from cryptography.fernet import Fernet
from io import BytesIO

app = Flask(__name__)

# Load RSA keys for JWT signing and verification
with open("private_key.pem", "r") as f:
    PRIVATE_KEY = f.read()

with open("public_key.pem", "r") as f:
    PUBLIC_KEY = f.read()

# In-memory store for UUID-to-JWT mapping
session_store = {}

def create_jwt(user_id):
    """
    Generates a JWT with a 1-hour expiration and unique session ID.
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

@app.route("/")
def index():
    """
    Renders the main page with the 'Generate QR Code' button.
    """
    return render_template("index.html")

@app.route("/generate_qr", methods=["POST"])
def generate_qr():
    data = request.json
    user_id = data.get("user_id")
    
    if not user_id:
        return jsonify({"error": "User ID required"}), 400
    
    # Generate a JWT and store it with a UUID
    token = create_jwt(user_id)
    session_id = str(uuid.uuid4())
    session_store[session_id] = token  # Store JWT associated with UUID
    
    # Generate a URL that points to the landing page with the UUID
    landing_url = f"http://127.0.0.1:5000/landing?session_id={session_id}"
    
    # Generate QR code with the URL
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


@app.route("/landing")
def landing():
    session_id = request.args.get("session_id")
    
    if session_id not in session_store:
        return "Invalid or expired session ID", 400
    
    # Retrieve the JWT from session_store
    token = session_store.get(session_id)
    
    try:
        # Verify JWT
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
        user_id = payload["sub"]
        return render_template("landing.html", user_id=user_id)
    except jwt.ExpiredSignatureError:
        return "Session expired! Please generate a new QR code.", 401
    except jwt.InvalidTokenError:
        return "Invalid token!", 400



if __name__ == "__main__":
    app.run(debug=True)
