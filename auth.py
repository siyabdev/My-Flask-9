from functools import wraps
from flask import request, jsonify, current_app
import jwt
from datetime import datetime, timedelta

# Secret key for JWT (in production, use environment variable)
SECRET_KEY = "your-secret-key-change-this-in-production"

def generate_token(user_id, username):
    """
    Generate a JWT token that expires in 24 hours
    """
    # Token expires in 24 hours
    expiration = datetime.utcnow() + timedelta(hours=24)
    
    # Create the token payload
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': expiration
    }
    
    # Generate token
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    # Convert to string if it's bytes (for compatibility)
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token

def verify_token(token):
    """
    Verify if a JWT token is valid
    Returns the payload if valid, None if invalid
    """
    try:
        # Decode and verify the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Token is invalid
        return None

def require_auth(f):
    """
    Decorator to protect routes that require authentication
    Use this on any route that needs JWT authentication
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                'code': 'NO_TOKEN',
                'message': 'No token provided. Please login first.'
            }), 401
        
        # Extract token from "Bearer <token>"
        try:
            token = auth_header.split(' ')[1]  # Gets the token part after "Bearer "
        except IndexError:
            return jsonify({
                'code': 'INVALID_TOKEN_FORMAT',
                'message': 'Token format is invalid. Use: Bearer <token>'
            }), 401
        
        # Verify the token
        payload = verify_token(token)
        
        if payload is None:
            return jsonify({
                'code': 'INVALID_TOKEN',
                'message': 'Token is invalid or expired. Please login again.'
            }), 401
        
        # Add user info to request so the route can use it
        request.user_id = payload['user_id']
        request.username = payload['username']
        
        # Continue to the actual route
        return f(*args, **kwargs)
    
    return decorated_function

