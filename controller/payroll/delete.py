from flask import Blueprint, request, jsonify
from crud.payroll.delete import delete_payroll_crud

payroll_delete_bp = Blueprint("payroll_delete_bp", __name__, url_prefix="/payroll")

#Delete payroll
@payroll_delete_bp.route("/delete", methods=["DELETE"])
def delete_payroll():
    data = request.json
    employee_id = data.get("employee_id")
    batch = data.get("batch")

    if not employee_id or not batch:
        return jsonify({"error": "Employee id and batch required"}), 400
    
    delete_query, payroll = delete_payroll_crud(employee_id=employee_id, batch=batch)

    try:
        if not payroll:
            return jsonify({
                "CODE": "PAYROLL_DOESNT_EXIST",
                "message": "Payroll doesnt exist, please enter a valid employee_id and batch"
            })
        if delete_query:
                return jsonify({
                        "CODE": "PAYROLL_DELETED",
                        "message": f"Payroll {employee_id}, '{batch}' is deleted"
                    })
    except Exception as error:
            print(f"error:{error}")
            return jsonify({
                "CODE":"EXCEPTIONAL_ERROR_OCCURED",
                "message":f"Exceptional error occured for payroll {employee_id}, '{batch}' deletion, please try again"
            })

