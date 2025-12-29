from flask import Blueprint, request, jsonify, current_app
from crud.payroll.update import update_payroll_crud
from utils.utils import get_payroll
from sqlalchemy.exc import IntegrityError
from schemas.payroll import UpdatePayrollRequest, PayrollResponse
from auth import require_auth

payroll_update_bp = Blueprint("payroll_update_bp", __name__, url_prefix="/payroll")

#Update payroll
@payroll_update_bp.route("/update", methods=["PUT"])
@require_auth
def update_payroll():
    data = UpdatePayrollRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error({"error": f"Schema error {message}."}), 400
        return jsonify({
            "code": "SCHEMA_ERROR",
            "message": f"Schema error occured {message}."
        }), 400

    if not data.has_any_updates():
        current_app.logger.error(f"Data {data} missing.")
        return jsonify({
            "code": "DATA_MISSING", 
            "message": f"Required fields for data {data} update are not provided"
        }), 400
    
    payroll = get_payroll(data.employee_id, data.batch)
    if not payroll:
        current_app.logger.error(f"Payroll {payroll} not found.")
        return jsonify({
            "code": "PAYROLL_NOT_FOUND", 
            "message": f"Payroll {payroll} not found."
            }), 404

    try:
        updated_payroll = update_payroll_crud(employee_id=data.employee_id, batch=data.batch, basic_salary=data.basic_salary, hourly_rate=data.hourly_rate, monthly_hours=data.monthly_hours, worked_hours=data.worked_hours, early=data.early, late=data.late, leaves=data.leaves, bonus1=data.bonus1, bonus2=data.bonus2)
        current_app.logger.info(f"Payroll updated {updated_payroll}.")
        return jsonify({
            "code": "PAYROLL_UPDATED",
            "message": PayrollResponse(updated_payroll).to_dict()
        }), 200
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        return jsonify({
            "code": "INTEGRITY_ERROR",
            "message": f"Integrity error occured {error}."
        }), 409
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        return jsonify({
            "code":"EXCEPTIONAL_ERROR_OCCURED",
            "message":f"Exceptional error {e} occured. Please try again."
        })