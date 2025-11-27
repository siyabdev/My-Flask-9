from flask import Flask, Blueprint, request, jsonify
from crud.employee.create import create_employee_crud
from utils.utils import get_employee
import logging
from sqlalchemy.exc import IntegrityError
from schemas.employee import CreateEmployeeRequest, EmployeeResponse, EmployeeListResponse

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

create_bp = Blueprint("create_bp", __name__, url_prefix="/employee")

#Create employee
@create_bp.route("/create", methods=["POST"])
def create_employee():
    data = CreateEmployeeRequest(request.json)

    if not data.is_valid():
        return jsonify({"error": "Missing fields"}), 400
    
    employee_by_username = get_employee(data.username)

    if employee_by_username:
        app.logger.error("Employee already exists.")
        return jsonify({
                "code": "EMPLOYEE_ALREADY_EXISTS",
                "message": f"This username {data.username} already exists, try a new one"
        }), 403

    try:
        new_employee = create_employee_crud(
            name=data.name,
            email=data.email,
            username=data.username,
            password=data.password,
            role=data.role
        )
    
        return jsonify({
            "code": "EMPLOYEE_CREATED",
            "data": EmployeeResponse(new_employee).to_dict()
        }), 201

    except IntegrityError as error:
        return jsonify({"code": "INTEGRITY_ERROR", "message": str(error)}), 409

    except Exception:
        return jsonify({"code": "ERROR"}), 500
