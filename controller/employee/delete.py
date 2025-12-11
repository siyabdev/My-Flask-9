from flask import Blueprint, request, jsonify, current_app
from crud.employee.delete import delete_employee_crud
from utils.utils import get_employee
from sqlalchemy.exc import IntegrityError
from schemas.employee import DeleteEmployeeRequest
from auth import require_auth

delete_bp = Blueprint("delete_bp", __name__, url_prefix="/employee")

#Delete employee
@delete_bp.route("/delete", methods=["DELETE"])
@require_auth
def delete_employee():
    data = DeleteEmployeeRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error(f"Schema error. {message}")
        return jsonify({
            "code": "SCHEMA_ERROR",
            "error": message
        }), 400

    employee_by_username = get_employee(data.username)

    if not employee_by_username:
        current_app.logger.info("Employee doesnt exist.")
        return jsonify({
            "CODE": "EMPLOYEE_DOESNT_EXIST",
            "message": "Employee doesnt exist, please enter a valid username"
        })

    try:
        delete_query = delete_employee_crud(data.username)
        if delete_query:
            current_app.logger.info("Employee deleted.")
            return jsonify({
                "CODE": "EMPLOYEE_DELETED",
                "message": f"Employee '{data.username}' is deleted"
            }), 200
    except IntegrityError as error:
        return jsonify({
            "CODE": "INTEGRITY_ERROR",
            "message": str(error)
        }), 409
    
    except Exception:
        return jsonify({"CODE": "ERROR"}), 500