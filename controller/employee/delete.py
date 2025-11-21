from flask import Blueprint, request, jsonify
from crud.employee.delete import delete_employee_crud

delete_bp = Blueprint("delete_bp", __name__, url_prefix="/employee")

#Delete employee
@delete_bp.route("/delete", methods=["DELETE"])
def delete_employee():
    data = request.json
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username required"}), 400

    delete_query, employee_by_username = delete_employee_crud(username=username)

    try:
        if not employee_by_username:
            return jsonify({
                "CODE": "EMPLOYEE_DOESNT_EXIST",
                "message": "Employee doesnt exist, please enter a valid username"
            })
        if delete_query:
                return jsonify({
                        "CODE": "EMPLOYEE_DELETED",
                        "message": f"Employee '{username}' is deleted"
                    })
    except Exception as error:
            print(f"error:{error}")
            return jsonify({
                "CODE":"EXCEPTIONAL_ERROR_OCCURED",
                "message":f"Exceptional error occured for employee '{username}' deletion, please try again"
            })