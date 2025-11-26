from flask import Flask, Blueprint, request, jsonify
from crud.employee.create import create_employee_crud
from utils.utils import get_employee
import logging
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.logger.setLevel(logging.INFO)


create_bp = Blueprint("create_bp", __name__, url_prefix="/employee")

#Create employee
@create_bp.route("/create", methods=["POST"])
def create_employee():

    data = request.json

    try: 

        name = data.get("name")
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        role = data.get("role", "guest")
    
        if not all([name, email, username, password, role]):
            app.logger.error("Missing fields.")
            return jsonify({"error": "Missing fields"}), 400
        
        employee_by_username = get_employee(username)

        if employee_by_username:
            app.logger.error("Employee already exists.")
            return jsonify({
                    "CODE": "EMPLOYEE_ALREADY_EXISTS",
                    "message": f"This username {username} already exists, try a new one"
            }), 403

        try:
            new_employee = create_employee_crud(
                name=name,
                email=email,
                username=username,
                password=password,
                role=role
            )
            
        except IntegrityError as error:
            app.logger.error("Inegrity error")
            return jsonify({
                "CODE":"INTEGRITY_ERROR_OCCURED",
                "message":f"Integrity error occured for employee '{username}' deletion, {error}"
            })
        
        if new_employee:
            app.logger.info("Employee Created.")
            return jsonify({
                "code": "EMPLOYEE_CREATED",
                "message": f"Employee '{name}' is created"
            })
        else:
            app.logger.error("Error.")
            return jsonify({
                "CODE":"ERROR",
                "messsage":f"Employee '{name}' is not created due to some error"
            })
    except Exception as error:
        print(f"error:{error}")
        app.logger.error("Exceptional error.")
        return jsonify({
            "CODE":"EXCEPTIONAL_ERROR_OCCURED",
            "message":f"Exceptional error occured for employee '{username}' deletion, please try again"
        })

