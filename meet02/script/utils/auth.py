from flask import request, jsonify
import os

VALID_API_KEYS = ["12345", "09876"]

def require_api_key(func):
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('Authorization')
        if not api_key or api_key.replace('Bearer ', '') not in VALID_API_KEYS:
            return jsonify({'error': 'Unauthorized'}), 401
        return func(*args, **kwargs)
    return decorated_function