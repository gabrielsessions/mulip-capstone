import jwt
import uuid
import datetime
import qrcode
from flask import Flask, request, jsonify, send_file, render_template
from io import BytesIO

app = Flask(__name__)

# Load RSA keys for JWT signing and verification
with open("private_key.pem", "r") as f:
    PRIVATE_KEY = f.read()

with open("public_key.pem", "r") as f:
    PUBLIC_KEY = f.read()

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

@app.route("/")
def index():
    """
    Renders the main page with the 'Generate QR Code' button.
    """
    return render_template("index.html")

@app.route("/generate_qr", methods=["POST"])
def generate_qr():
    """
    Generates a QR code with a URL pointing to the landing page.
    """
    # URL for the landing page (no session ID, no data stored on the server)
    landing_url = f"http://127.0.0.1:5000/landing"
    
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
    """
    Generates a JWT for the user upon loading the landing page and embeds it in the template.
    """
    user_id = "user123"  # Example user ID; this could be dynamic based on login info or other data
    token = create_jwt(user_id)
    
    # Pass the JWT to the template
    return render_template("landing.html", jwt_token=token)

if __name__ == "__main__":
    app.run(debug=True)
