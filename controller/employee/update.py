from flask import Blueprint, request, jsonify, current_app
from crud.employee.update import update_employee_crud
from utils.utils import get_employee
from sqlalchemy.exc import IntegrityError
from schemas.employee import UpdateEmployeeRequest, EmployeeResponse
from auth import require_auth

update_bp = Blueprint("update_bp", __name__, url_prefix="/employee")

#Update employee
@update_bp.route("/update", methods=["PUT"])
@require_auth
def update_employee():
    data = UpdateEmployeeRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error(f"Schema error. {message}")
        return jsonify({
            "code": "SCHEMA_ERROR",
            "error": message
        }), 400

    if not data.has_any_updates():
        current_app.logger.error("Data missing.")
        return jsonify({
            "code": "DATA_MISSING", 
            "error": "Required fields for data update not provided"
            }), 400
    
    employee = get_employee(data.username)
    if not employee:
        current_app.logger.error("Employee not found.")
        return jsonify({
            "code": "EMPLOYEE_NOT_FOUND", 
            "error": "Required fields for data update not provided"
            }), 404

    try:        
        updated_employee = update_employee_crud(username=data.username, name=data.name, password=data.password, role=data.role, email=data.email)
        current_app.logger.info("Employee updated.")
        return jsonify({
            "code": "EMPLOYEE_UPDATED",
            "data": EmployeeResponse(updated_employee).to_dict()
        }), 200

    except IntegrityError as error:
        return jsonify({
            "code": "INTEGRITY_ERROR",
            "message": str(error)
        }), 409
    
    except Exception:
        return jsonify({"code": "ERROR"}), 500