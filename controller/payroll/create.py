from flask import Blueprint, request, jsonify, current_app
from crud.payroll.create import create_payroll_crud
from utils.utils import get_payroll
from sqlalchemy.exc import IntegrityError
from schemas.payroll import CreatePayrollRequest, PayrollResponse
from auth import require_auth

payroll_create_bp = Blueprint("payroll_create_bp", __name__, url_prefix="/payroll")

#Create payroll
@payroll_create_bp.route("/create", methods=["POST"])
@require_auth
def create_payroll():
    data = CreatePayrollRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error(f"Schema error {message}."), 400
        return jsonify({
            "code": "SCHEMA_ERROR",
            "message": f"Schema error occured {message}."
        }), 400

    checking_payroll = get_payroll(data.employee_id, data.batch)

    if checking_payroll: 
        current_app.logger.info(f"Payroll {checking_payroll} already exists.")
        return jsonify({
            "code": "PAYROLL_ALREADY_EXISTS",
            "message": f"This payroll {data.employee_id}, '{data.batch}' already exists, try a new one."
        }), 403
    
    try:
        new_payroll = create_payroll_crud(
            employee_id = data.employee_id,
            batch = data.batch,
            basic_salary = data.basic_salary,
            hourly_rate = data.hourly_rate,
            monthly_hours = data.monthly_hours,
            worked_hours = data.worked_hours,
            early = data.early,
            late = data.late,
            leaves = data.leaves,
            bonus1 = data.bonus1,
            bonus2 = data.bonus2
        )

        current_app.logger.info(f"Payroll {new_payroll} created.")
        return jsonify({
            "code": "PAYROLL_CREATED",
            "data": PayrollResponse(new_payroll).to_dict()
        }), 201
    
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
