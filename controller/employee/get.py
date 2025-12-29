from flask import Blueprint, request, jsonify, current_app
from crud.employee.get import get_employee_crud, get_employees_crud, get_employee_short_crud
from schemas.employee import EmployeeResponse, EmployeeListResponse, EmployeeShortResponse
from sqlalchemy.exc import IntegrityError
from auth import require_auth

get_bp = Blueprint("get_bp", __name__, url_prefix="/employee")

#Get employee
@get_bp.route("/get", methods=["GET"])
@require_auth
def get_employee():
    data = request.json
    username = data.get("username")

    if not username:
        current_app.logger.error(f"No username '{username}' provided for employee.")
        return jsonify({
            "code": "NO_USERNAME_PROVIDED",
            "message": f"Please enter username '{username}'."
        }), 403
    
    employee = get_employee_crud(username=username)

    try:
        if employee:
            current_app.logger.info(f"Employee {employee} response returned.")
            return EmployeeResponse(employee).to_dict()
        
        else:
            current_app.logger.error(f"Username '{username}' not registered.")
            return jsonify({
                "code":"USERNAME_DOESNT_EXIST",
                "message": f"Username '{username}' is not registered, please try another."
            }), 403
    
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
                "message":f"Exceptional error {e} occured. please try again."
            })
    

#Get all employees
@get_bp.route("/all", methods=["GET"])
@require_auth
def get_all_employees():
     
    try:
         get_employees = get_employees_crud()

         if get_employees:
              current_app.logger.info(f"Employees {get_employees} response returned.")
              return EmployeeListResponse.from_list(get_employees)
         else:
            current_app.logger.error("No employees found.")
            return jsonify({
                "code":"NO_EMPLOYEES_FOUND",
                "message":"No employees found, please add employee first."
            })
    
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

#Get short details (employee)
@get_bp.route("/short", methods = ["GET"])
@require_auth
def get_employee_short():

    try:
        employees = get_employee_short_crud()

        if employees:
            current_app.logger.info(f"Employees {employees} response returned.")
            return EmployeeShortResponse.from_list(employees)

        else:
            current_app.logger.error("No employees found")
            return jsonify({
                "code":"NO_EMPLOYEES_FOUND",
                "message":"No employees found, please add employee first."
            })
    
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