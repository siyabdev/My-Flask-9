from flask import Blueprint, request, jsonify
from crud.payroll.update import update_payroll_crud

payroll_update_bp = Blueprint("payroll_update_bp", __name__, url_prefix="/payroll")

#Update payroll
@payroll_update_bp.route("/update", methods=["PUT"])
def update_payroll():
    data = request.json

    employee_id = data.get("employee_id")
    batch = data.get("batch")
    basic_salary = data.get("basic_salary")
    hourly_rate = data.get("hourly_rate")
    monthly_hours = data.get("monthly_hours")
    worked_hours = data.get("worked_hours")
    early = data.get("early")
    late = data.get("late")
    leaves = data.get("leaves")
    bonus1 = data.get("bonus1")
    bonus2 = data.get("bonus2")

    if not employee_id or not batch:
        return jsonify({"error": "Employee id or batch required"}), 400
    
    payroll = update_payroll_crud(employee_id=employee_id, batch=batch, basic_salary=basic_salary, hourly_rate=hourly_rate, monthly_hours=monthly_hours, worked_hours=worked_hours, early=early, late=late, leaves=leaves, bonus1=bonus1, bonus2=bonus2)

    try:
        if not payroll:
            return jsonify({"error": "Payroll not found"}), 404
        
        if payroll:
            return jsonify({
                    "CODE": "PAYROLL_UPDATED",
                    "message": f"Payroll {employee_id}, '{batch}' is updated"
                })
             
    except Exception as error:
            print(f"error:{error}")
            return jsonify({
                "CODE":"EXCEPTIONAL_ERROR_OCCURED",
                "message":f"Exceptional error occured for payroll {employee_id} '{batch}' update, please try again"
            })