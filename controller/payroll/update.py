from flask import Flask, Blueprint, request, jsonify
from crud.payroll.update import update_payroll_crud
from utils.utils import get_payroll
from sqlalchemy.exc import IntegrityError
from schemas.payroll import UpdatePayrollRequest, PayrollResponse
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

payroll_update_bp = Blueprint("payroll_update_bp", __name__, url_prefix="/payroll")

#Update payroll
@payroll_update_bp.route("/update", methods=["PUT"])
def update_payroll():
    data = UpdatePayrollRequest(request.json)

    if not data.has_employee_id() or not data.has_batch:
        return jsonify({
            "code": "ESSENTIALS_REQUIRED", 
            "error": "Employee_id and Batch required"
            }), 400

    if not data.has_any_updates():
        return jsonify({
            "code": "DATA_MISSING", 
            "error": "Required fields for data update not provided"
            }), 400
    
    payroll = get_payroll(data.employee_id, data.batch)
    if not payroll:
        return jsonify({
            "code": "PAYROLL_NOT_FOUND", 
            "error": "Required fields for data update not provided"
            }), 404

    try:
        updated_payroll = update_payroll_crud(employee_id=data.employee_id, batch=data.batch, basic_salary=data.basic_salary, hourly_rate=data.hourly_rate, monthly_hours=data.monthly_hours, worked_hours=data.worked_hours, early=data.early, late=data.late, leaves=data.leaves, bonus1=data.bonus1, bonus2=data.bonus2)
            
        return jsonify({
            "code": "PAYROLL_UPDATED",
            "data": PayrollResponse(updated_payroll).to_dict()
        }), 200
    
    except IntegrityError as error:
        return jsonify({
            "code": "INTEGRITY_ERROR",
            "message": str(error)
        }), 409
    
    except Exception:
        return jsonify({"code": "ERROR"}), 500