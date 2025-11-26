from flask import Flask, Blueprint, request, jsonify
from crud.employee.delete import delete_employee_crud
from utils.utils import get_employee
import logging
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

delete_bp = Blueprint("delete_bp", __name__, url_prefix="/employee")

#Delete employee
@delete_bp.route("/delete", methods=["DELETE"])
def delete_employee():
    data = request.json
    username = data.get("username")

    if not username:
        app.logger.error("Username required")
        return jsonify({"error": "Username required"}), 400
    

    employee_by_username = get_employee(username)

    if not employee_by_username:
        app.logger.info("Employee doesnt exist.")
        return jsonify({
            "CODE": "EMPLOYEE_DOESNT_EXIST",
            "message": "Employee doesnt exist, please enter a valid username"
        })

    try:
        delete_query = delete_employee_crud(username=username)
        
    except IntegrityError as error:
        app.logger.error("Integrirty error")
        return jsonify({
            "CODE":"INTEGRITY_ERROR_OCCURED",
            "message":f"INTEGRITY error occured for employee '{username}' deletion, {error}"
        })

    try:
        if delete_query:
                app.logger.info("Employee deleted")
                return jsonify({
                        "CODE": "EMPLOYEE_DELETED",
                        "message": f"Employee '{username}' is deleted"
                    })
    except Exception as error:
            print(f"error:{error}")
            app.logger.error("Exceptional error")
            return jsonify({
                "CODE":"EXCEPTIONAL_ERROR_OCCURED",
                "message":f"Exceptional error occured for employee '{username}' deletion, please try again"
            })