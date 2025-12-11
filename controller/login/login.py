from flask import Blueprint, request, jsonify, current_app
from crud.login.login import verify_login
from schemas.login import LoginRequest, LoginResponse
from auth import generate_token

# Create blueprint for login
login_bp = Blueprint("login_bp", __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    data = LoginRequest(request.json)
    valid, message = data.is_valid()
    
    if not valid:
        current_app.logger.error(f"Login schema error: {message}")
        return jsonify({
            "code": "SCHEMA_ERROR",
            "error": message
        }), 400
    
    employee = verify_login(data.username, data.password)
    
    if not employee:
        current_app.logger.info(f"Login failed for username: {data.username}")
        return jsonify({
            "code": "LOGIN_FAILED",
            "message": "Invalid username or password"
        }), 401
    
    token = generate_token(employee.id, employee.username)
    
    current_app.logger.info(f"Login successful for username: {data.username}")
    
    response = LoginResponse(token, employee.id, employee.username)
    return jsonify({
        "code": "LOGIN_SUCCESS",
        "message": "Login successful",
        "data": response.to_dict()
    }), 200