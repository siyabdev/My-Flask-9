from flask import Blueprint, request, jsonify, current_app
from crud.employee.create import create_employee_crud
from utils.utils import get_employee
from sqlalchemy.exc import IntegrityError
from schemas.employee import CreateEmployeeRequest, EmployeeResponse

create_bp = Blueprint("create_bp", __name__, url_prefix="/employee")

#Create employee
@create_bp.route("/create", methods=["POST"])
def create_employee():
    data = CreateEmployeeRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error(f"Schema error. {message}"),400
        return jsonify({"error": f"Schema error. {message}"}), 400
    
    
    employee_by_username = get_employee(data.username)

    if employee_by_username:
        current_app.logger.info("Employee already exists.")
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

        current_app.logger.info(f"employee created: {new_employee}")
        return jsonify({
            "code": "EMPLOYEE_CREATED",
            "data": EmployeeResponse(new_employee).to_dict()
        }), 201

    except IntegrityError as error:
        return jsonify({"code": "INTEGRITY_ERROR", "message": str(error)}), 409

    except Exception:
        return jsonify({"code": "ERROR"}), 500
