from flask import Flask, jsonify
import hashlib
import hmac
import secrets
import string
import time

app = Flask(__name__)

WORK_FACTOR = 2_000_000
PASSWORD_LENGTH = 10
SALT_SIZE_BYTES = 16


def generate_random_password(length):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


USERNAME = "demo_user"
USER_PASSWORD = generate_random_password(PASSWORD_LENGTH)
PASSWORD_SALT = secrets.token_bytes(SALT_SIZE_BYTES)

STORED_PASSWORD_HASH = hashlib.pbkdf2_hmac(
    "sha256",
    USER_PASSWORD.encode("utf-8"),
    PASSWORD_SALT,
    WORK_FACTOR
)


@app.route("/")
def home():
    return "Server is running..."


@app.route("/login-check")
def login_check():
    start_time = time.perf_counter()

    login_password = USER_PASSWORD

    calculated_hash = hashlib.pbkdf2_hmac(
        "sha256",
        login_password.encode("utf-8"),
        PASSWORD_SALT,
        WORK_FACTOR
    )

    password_verified = hmac.compare_digest(
        calculated_hash,
        STORED_PASSWORD_HASH
    )

    execution_time = time.perf_counter() - start_time

    return jsonify({
        "Account and Login Input": {
            "username": USERNAME,
            "password": login_password
        },
        "Password Security Parameters": {
            "algorithm": "PBKDF2-HMAC-SHA256",
            "work_factor": WORK_FACTOR,
            "password_length": PASSWORD_LENGTH,
            "salt_size_bytes": SALT_SIZE_BYTES
        },
        "Password Hash": calculated_hash.hex(),
        "Verification Output": password_verified,
        "Execution Time": f"{execution_time:.4f} seconds"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
