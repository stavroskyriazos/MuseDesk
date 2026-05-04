from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from .models import User, db


auth = Blueprint("auth", __name__)


@auth.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 409

    role = "admin" if User.query.count() == 0 else "user"
    user = User(
        username=username,
        password=generate_password_hash(password),
        role=role,
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered",
        "user_id": user.id,
        "role": user.role,
    }), 201


@auth.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return jsonify({
            "message": "Login successful",
            "user_id": user.id,
            "role": user.role,
            "username": user.username,
        })

    return jsonify({"message": "Invalid credentials"}), 401
