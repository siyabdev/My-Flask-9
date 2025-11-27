from flask import Flask, Blueprint, request, jsonify
from crud.payroll.update import update_payroll_crud
from sqlalchemy.exc import IntegrityError
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

payroll_update_bp = Blueprint("payroll_update_bp", __name__, url_prefix="/payroll")

#Update payroll
@payroll_update_bp.route("/update", methods=["PUT"])
def update_payroll():
    data = request.json

    try:
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
            app.logger.error("Id or batch required")
            return jsonify({"error": "Employee id or batch required"}), 400
        
        try:
            payroll = update_payroll_crud(employee_id=employee_id, batch=batch, basic_salary=basic_salary, hourly_rate=hourly_rate, monthly_hours=monthly_hours, worked_hours=worked_hours, early=early, late=late, leaves=leaves, bonus1=bonus1, bonus2=bonus2)
        
            if not payroll:
                app.logger.error("No payroll")
                return jsonify({"error": "Payroll not found"}), 404
            
            if payroll:
                app.logger.info("Payroll updated")
                return jsonify({
                        "CODE": "PAYROLL_UPDATED",
                        "message": f"Payroll {employee_id}, '{batch}' is updated"
                    })       
        except IntegrityError as error:
            app.logger.error("Integrirty error")
            return jsonify({
                "CODE":"INTEGRITY_ERROR_OCCURED",
                "message":f"INTEGRITY error occured for payroll {employee_id}, '{batch}' deletion, {error}"
            })
          
    except Exception as error:
            print(f"error:{error}")
            app.logger.error("Exceptional error")
            return jsonify({
                "CODE":"EXCEPTIONAL_ERROR_OCCURED",
                "message":f"Exceptional error occured for payroll {employee_id} '{batch}' update, please try again"
            })