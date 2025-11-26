from flask import Flask, Blueprint, request, jsonify
from crud.employee.get import get_employee_crud, get_employees_crud
from models import Employee
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

get_bp = Blueprint("get_bp", __name__, url_prefix="/employee")

#Get employee
@get_bp.route("/get", methods=["GET"])
def get_employee():
    data = request.json
    username = data.get("username")

    if not username:
        app.logger.error("No username provided for employee")
        return jsonify({
            "CODE":"NO_USERNAME_PROVIDED",
            "message":"Please enter username"
        }), 403
    
    employee = get_employee_crud(username=username)

    print(f"employee:{employee}")

    try:
        if employee:
            return employee.to_dict()
        
        else:
            app.logger.error("Username is not registered")
            return jsonify({
                "CODE":"USERNAME_DOESNT_EXIST",
                "message": f"Please try another username, {username} is not registered"
            }), 403

    except Exception as error:
            print(f"error:{error}")
            app.logger.error("Exceptional error.")
            return jsonify({
                "CODE":"EXCEPTIONAL_ERROR_OCCURED",
                "message":f"Exceptional error occured for getting employee '{username}', please try again"
            })

#Get all employees
@get_bp.route("/all", methods=["GET"])
def get_all_employees():
     
    try:
         get_employees = get_employees_crud()

         if get_employees:
              return Employee.to_dict_list(get_employees)
         else:
            app.logger.error("No employees found")
            return jsonify({
                "CODE":"NO_EMPLOYEES_FOUND",
                "message":"No employees found, please add employee first"
            })
    except Exception as error:
        print(f"error:{error}")
        app.logger.error("Exceptional error.")
        return jsonify({
            "CODE":"EXCEPTIONAL_ERROR_OCCURED",
            "message":"Exceptional error occured for getting all employees, please try again"
        })
    
