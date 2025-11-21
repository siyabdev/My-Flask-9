from flask import Blueprint, request, jsonify
from crud.employee.create import create_employee_crud
from models import Employee

create_bp = Blueprint("create_bp", __name__, url_prefix="/employee")


def get_employee(username):
    employee = Employee.query.filter_by(username=username).first()
    return employee

#Create employee
@create_bp.route("/create", methods=["POST"])
def create_employee():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "guest")

    if not all([name, email, username, password, role]):
        return jsonify({"error": "Missing fields"}), 400
    
    employee_by_username = get_employee(username)

    if employee_by_username: 
        return jsonify({
                "CODE": "EMPLOYEE_ALREADY_EXISTS",
                "message": f"This {username} already exists, try a new one"
        }), 403

    new_employee = create_employee_crud(
        name=name,
        email=email,
        username=username,
        password=password,
        role=role
    )
    try:
        if new_employee:
            return jsonify({
                "code": "EMPLOYEE_CREATED",
                "message": f"Employee '{name}' is created"
            })
        else:
            return jsonify({
                "CODE":"ERROR",
                "messsage":f"Employee '{name}' is not created due to some error"
            })
    except Exception as error:
        print(f"error:{error}")
        return jsonify({
            "CODE":"EXCEPTIONAL_ERROR_OCCURED",
            "message":f"Exceptional error occured for employee '{name}' creation, please try again"
        })