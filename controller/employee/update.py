from flask import Blueprint, request, jsonify
from crud.employee.update import update_employee_crud

update_bp = Blueprint("update_bp", __name__, url_prefix="/employee")

#Update employee
@update_bp.route("/update", methods=["PUT"])
def update_employee():
    data = request.json
    username = data.get("username")
    name = data.get("name")
    email = data.get("email")
    role = data.get("role")
    password = data.get("password")

    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    employee = update_employee_crud(username=username, name=name, password=password, role=role, email=email)

    try:
        if not employee:
            return jsonify({"error": "Employee not found"}), 404
        
        if employee:
            return jsonify({
                    "CODE": "EMPLOYEE_UPDATED",
                    "message": f"Employee '{username}' is updated"
                })
             
    except Exception as error:
            print(f"error:{error}")
            return jsonify({
                "CODE":"EXCEPTIONAL_ERROR_OCCURED",
                "message":f"Exceptional error occured for employee '{username}' update, please try again"
            })