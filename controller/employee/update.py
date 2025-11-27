from flask import Flask, Blueprint, request, jsonify
from crud.employee.update import update_employee_crud
from utils.utils import get_employee
from sqlalchemy.exc import IntegrityError
from schemas.employee import UpdateEmployeeRequest, EmployeeResponse
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

update_bp = Blueprint("update_bp", __name__, url_prefix="/employee")

#Update employee
@update_bp.route("/update", methods=["PUT"])
def update_employee():
    data = UpdateEmployeeRequest(request.json)

    if not data.has_username():
        return jsonify({
            "code": "USERNAME_REQUIRED", 
            "error": "Username required"
            }), 400

    if not data.has_any_updates():
        return jsonify({
            "code": "DATA_MISSING", 
            "error": "Required fields for data update not provided"
            }), 400
    
    employee = get_employee(data.username)
    if not employee:
        return jsonify({
            "code": "EMPLOYEE_NOT_FOUND", 
            "error": "Required fields for data update not provided"
            }), 404

    try:        
        updated_employee = update_employee_crud(username=data.username, name=data.name, password=data.password, role=data.role, email=data.email)

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