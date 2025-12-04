from flask import Blueprint, request, jsonify, current_app
from crud.payroll.create import create_payroll_crud
from utils.utils import get_payroll
from sqlalchemy.exc import IntegrityError
from schemas.payroll import CreatePayrollRequest, PayrollResponse

payroll_create_bp = Blueprint("payroll_create_bp", __name__, url_prefix="/payroll")

#Create payroll
@payroll_create_bp.route("/create", methods=["POST"])
def create_payroll():
    data = CreatePayrollRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error(f"Schema error. {message}"), 400
        return jsonify({"error": f"Schema error. {message}"}), 400

    checking_payroll = get_payroll(data.employee_id, data.batch)

    if checking_payroll: 
        current_app.logger.info("Payroll already exists.")
        return jsonify({
                "CODE": "PAYROLL_ALREADY_EXISTS",
                "message": f"This payroll {data.employee_id}, '{data.batch}' already exists, try a new one"
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
        current_app.logger.info("Payroll created.")
        return jsonify({
            "CODE": "PAYROLL_CREATED",
            "data": PayrollResponse(new_payroll).to_dict()
        }), 201

    except IntegrityError as error:
        current_app.logger.error("Integrity error")
        return jsonify({"CODE": "INTEGRITY_ERROR", "message": str(error)}), 409

    except Exception:
        current_app.logger.error("Exceptional error")
        return jsonify({"CODE": "EXCEPTIONAL_ERROR"}), 500
