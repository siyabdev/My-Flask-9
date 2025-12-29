from flask import Blueprint, request, jsonify, current_app
from crud.login.login import verify_login
from schemas.login import LoginRequest, LoginResponse
from auth import generate_token
from sqlalchemy.exc import IntegrityError

#Create blueprint for login
login_bp = Blueprint("login_bp", __name__)

#Login
@login_bp.route("/login", methods=["POST"])
def login():
    data = LoginRequest(request.json)
    valid, message = data.is_valid()
    
    if not valid:
        current_app.logger.error(f"Login schema error {message}.")
        return jsonify({
            "code": "SCHEMA_ERROR",
            "message": f"Login schema error occured {message}.."
        }), 400
    
    employee = verify_login(data.username, data.password)
    
    if not employee:
        current_app.logger.error(f"Login failed for username '{data.username}'.")
        return jsonify({
            "code": "LOGIN_FAILED",
            "message": f"Invalid username '{data.username}' or password '{data.password}' provided."
        }), 401
    
    try:
        token = generate_token(employee.id, employee.username)
        
        response = LoginResponse(token, employee.id, employee.username)

        current_app.logger.info(f"Login successful for username '{data.username}'.")
        return jsonify({
            "code": "LOGIN_SUCCESS",
            "message": f"Login successful for username {data.username}.",
            "data": response.to_dict()
        }), 200
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        return jsonify({
            "code": "INTEGRITY_ERROR",
            "message": f"Integrity error occured {error}."
        }), 409
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        return jsonify({
            "code":"EXCEPTIONAL_ERROR_OCCURED",
            "message":f"Exceptional error {e} occured. Please try again."
        })