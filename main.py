from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import hashlib
import time

app = Flask(__name__)

# Rate Limiting
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[]
)

# Work factor
WORK_FACTOR = 2_000_000


@app.route("/")
def home():
    return jsonify({
        "message": "Cybersecurity Lab",
        "status": "running",
        "work_factor": WORK_FACTOR
    })


@app.route("/login-check")
@limiter.limit("5 per second")
def login_check():

    # จำลองการคำนวณที่ใช้ทรัพยากร CPU
    data = b"cybersecurity-lab"

    result = data

    for _ in range(WORK_FACTOR):
        result = hashlib.sha256(result).digest()

    return jsonify({
        "status": "success",
        "message": "Login check completed",
        "work_factor": WORK_FACTOR
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)