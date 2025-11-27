from flask import Flask, Blueprint, request, jsonify
from crud.payroll.create import create_payroll_crud
from utils.utils import get_employee_by_employee_id
from utils.utils import get_payroll
import logging
from sqlalchemy.exc import IntegrityError
from schemas.payroll import CreatePayrollRequest, PayrollResponse, PayrollListResponse

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

payroll_create_bp = Blueprint("payroll_create_bp", __name__, url_prefix="/payroll")

#Create payroll
@payroll_create_bp.route("/create", methods=["POST"])
def create_payroll():
    data = CreatePayrollRequest(request.json)


    if not data.is_valid():
        return jsonify({"error": "Missing fields"}), 400

    checking_payroll = get_payroll(data.employee_id, data.batch)
    if checking_payroll: 
        app.logger.info("Payroll already exists.")
        return jsonify({
                "CODE": "PAYROLL_ALREADY_EXISTS",
                "message": f"This payroll {data.employee_id}, '{data.batch}' already exists, try a new one"
        })

    checking_employee = get_employee_by_employee_id(data.employee_id)

    print(checking_employee)

    if not checking_employee:
        app.logger.error("No employee.")
        return jsonify({
                "CODE": "EMPLOYEE_NOT_FOUND",
                "message": f"Employee {data.employee_id} not found, try a new one"
        }), 404
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
    
        return jsonify({
            "code": "PAYROLL_CREATED",
            "data": PayrollResponse(new_payroll).to_dict()
        }), 201

    except IntegrityError as error:
        return jsonify({"code": "INTEGRITY_ERROR", "message": str(error)}), 409

    except Exception:
        return jsonify({"code": "ERROR"}), 500
