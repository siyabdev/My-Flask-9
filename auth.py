from functools import wraps
from flask import request, jsonify, current_app
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "siyabiqbaljibran"

def generate_token(user_id, username):
    expiration = datetime.utcnow() + timedelta(hours=24)
    
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': expiration
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                'code': 'NO_TOKEN',
                'message': 'No token provided. Please login first.'
            }), 401
        
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return jsonify({
                'code': 'INVALID_TOKEN_FORMAT',
                'message': 'Token format is invalid. Use: Bearer <token>'
            }), 401
        
        payload = verify_token(token)
        
        if payload is None:
            return jsonify({
                'code': 'INVALID_TOKEN',
                'message': 'Token is invalid or expired. Please login again.'
            }), 401
        
        request.user_id = payload['user_id']
        request.username = payload['username']
        
        return f(*args, **kwargs)
    
    return decorated_function