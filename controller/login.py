from flask import Blueprint, request, jsonify, current_app
from crud.login import verify_login
from schemas.login import LoginRequest, LoginResponse
from auth import generate_token

# Create blueprint for login
login_bp = Blueprint("login_bp", __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    """
    Login endpoint
    Checks username and password, returns JWT token if valid
    """
    # Get and validate request data
    data = LoginRequest(request.json)
    valid, message = data.is_valid()
    
    if not valid:
        current_app.logger.error(f"Login schema error: {message}")
        return jsonify({
            "code": "SCHEMA_ERROR",
            "error": message
        }), 400
    
    # Verify username and password
    employee = verify_login(data.username, data.password)
    
    if not employee:
        current_app.logger.info(f"Login failed for username: {data.username}")
        return jsonify({
            "code": "LOGIN_FAILED",
            "message": "Invalid username or password"
        }), 401
    
    # Generate JWT token (valid for 24 hours)
    token = generate_token(employee.id, employee.username)
    
    current_app.logger.info(f"Login successful for username: {data.username}")
    
    # Return token and user info
    response = LoginResponse(token, employee.id, employee.username)
    return jsonify({
        "code": "LOGIN_SUCCESS",
        "message": "Login successful",
        "data": response.to_dict()
    }), 200

