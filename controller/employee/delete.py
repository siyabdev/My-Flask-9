from flask import Flask, Blueprint, request, jsonify
from crud.employee.delete import delete_employee_crud
from utils.utils import get_employee
import logging
from sqlalchemy.exc import IntegrityError
from schemas.employee import DeleteEmployeeRequest

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

delete_bp = Blueprint("delete_bp", __name__, url_prefix="/employee")

#Delete employee
@delete_bp.route("/delete", methods=["DELETE"])
def delete_employee():
    data = DeleteEmployeeRequest(request.json)

    if not data.is_valid():
        return jsonify({"error": "Username required"}), 400

    employee_by_username = get_employee(data.username)

    if not employee_by_username:
        app.logger.info("Employee doesnt exist.")
        return jsonify({
            "CODE": "EMPLOYEE_DOESNT_EXIST",
            "message": "Employee doesnt exist, please enter a valid username"
        })

    try:
        delete_query = delete_employee_crud(data.username)

        if delete_query:
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