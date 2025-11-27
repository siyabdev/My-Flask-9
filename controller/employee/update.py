from flask import Flask, Blueprint, request, jsonify
from crud.employee.update import update_employee_crud
from sqlalchemy.exc import IntegrityError
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

update_bp = Blueprint("update_bp", __name__, url_prefix="/employee")

#Update employee
@update_bp.route("/update", methods=["PUT"])
def update_employee():
    data = request.json

    try:
        username = data.get("username")
        name = data.get("name")
        email = data.get("email")
        role = data.get("role")
        password = data.get("password")

        if not username:
            app.logger.error("Username required")
            return jsonify({"error": "Username is required"}), 400
        try:        
            employee = update_employee_crud(username=username, name=name, password=password, role=role, email=email)

            if not employee:
                app.logger.error("No employee")
                return jsonify({"error": "Employee not found"}), 404
        except IntegrityError as error:
            app.logger.error("integrity error")
            return jsonify({
                "CODE":"integrity_ERROR_OCCURED",
                "message":f"integrity error occured for employee '{username}' deletion, {error}"
            })
        
        if employee:
            app.logger.info("Employee updated")
            return jsonify({
                    "CODE": "EMPLOYEE_UPDATED",
                    "message": f"Employee '{username}' is updated"
                })
    except Exception as error:
            print(f"error:{error}")
            app.logger.error("Exceptional error")
            return jsonify({
                "CODE":"EXCEPTIONAL_ERROR_OCCURED",
                "message":f"Exceptional error occured for employee '{username}' update, please try again"
            })