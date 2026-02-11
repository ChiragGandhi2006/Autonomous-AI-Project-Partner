from functools import wraps
from flask import request, jsonify


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token or token != "SECRET_TOKEN":
            return jsonify({"error": "Unauthorized"}), 401

        return func(*args, **kwargs)
    return wrapper
