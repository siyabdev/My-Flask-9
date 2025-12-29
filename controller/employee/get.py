from flask import Blueprint, request, jsonify, current_app
from crud.employee.get import get_employee_crud, get_employees_crud, get_employee_short_crud
from schemas.employee import EmployeeResponse, EmployeeListResponse, EmployeeShortResponse
from auth import require_auth

get_bp = Blueprint("get_bp", __name__, url_prefix="/employee")

#Get employee
@get_bp.route("/get", methods=["GET"])
@require_auth
def get_employee():
    data = request.json
    username = data.get("username")

    if not username:
        current_app.logger.error("No username provided for employee")
        return jsonify({
            "CODE":"NO_USERNAME_PROVIDED",
            "message":"Please enter username"
        }), 403
    
    employee = get_employee_crud(username=username)

    try:
        if employee:
            return EmployeeResponse(employee).to_dict()
        
        else:
            current_app.logger.error("Username is not registered")
            return jsonify({
                "CODE":"USERNAME_DOESNT_EXIST",
                "message": f"Please try another username, {username} is not registered"
            }), 403

    except Exception as error:
            print(f"error:{error}")
            current_app.logger.error("Exceptional error.")
            return jsonify({
                "CODE":"EXCEPTIONAL_ERROR_OCCURED",
                "message":f"Exceptional error occured for getting employee '{username}', please try again"
            })

#Get all employees
@get_bp.route("/all", methods=["GET"])
@require_auth
def get_all_employees():
     
    try:
         get_employees = get_employees_crud()

         if get_employees:
              return EmployeeListResponse.build(get_employees)
         else:
            current_app.logger.error("No employees found")
            return jsonify({
                "CODE":"NO_EMPLOYEES_FOUND",
                "message":"No employees found, please add employee first"
            })
    except Exception as error:
        current_app.logger.error("Exceptional error.")
        return jsonify({
            "CODE":"EXCEPTIONAL_ERROR_OCCURED",
            "message":"Exceptional error occured for getting all employees, please try again"
        })

#Get short details (employee)
@get_bp.route("/short", methods = ["GET"])
@require_auth
def get_employee_short():

    try:
        employees = get_employee_short_crud()

        if employees:
            return EmployeeShortResponse(employees).to_dict()
        else:
            current_app.logger.error("No employees found")
            return jsonify({
                "CODE":"NO_EMPLOYEES_FOUND",
                "message":"No employees found, please add employee first"
            })
    except Exception as error:
        current_app.logger.error(f"Exceptional error. {error}")
        return jsonify({
            "CODE":"EXCEPTIONAL_ERROR_OCCURED",
            "message":"Exceptional error occured for getting all employees, please try again"
        })