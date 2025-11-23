from flask import Blueprint, request, jsonify
from crud.payroll.create import create_payroll_crud
from utils.utils import get_employee_by_employee_id
from utils.utils import get_payroll

payroll_create_bp = Blueprint("payroll_create_bp", __name__, url_prefix="/payroll")

#Create payroll
@payroll_create_bp.route("/create", methods=["POST"])
def create_payroll():
    data = request.json

    print(f"data: {data}")

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

    if not all([employee_id, batch, basic_salary, hourly_rate, monthly_hours, worked_hours, early, late, leaves, bonus1, bonus2]):
        return jsonify({"error": "Missing fields"}), 400

    checking_payroll = get_payroll(employee_id, batch)
    if checking_payroll: 
        return jsonify({
                "CODE": "PAYROLL_ALREADY_EXISTS",
                "message": f"This payroll {employee_id}, '{batch}' already exists, try a new one"
        })

    checking_employee = get_employee_by_employee_id(employee_id)

    print(checking_employee)

    if not checking_employee:
        return jsonify({
                "CODE": "EMPLOYEE_NOT_FOUND",
                "message": f"Employee {employee_id} not found, try a new one"
        }), 404

    new_payroll = create_payroll_crud(
        employee_id = employee_id,
        batch = batch,
        basic_salary = basic_salary,
        hourly_rate = hourly_rate,
        monthly_hours = monthly_hours,
        worked_hours = worked_hours,
        early = early,
        late = late,
        leaves = leaves,
        bonus1 = bonus1,
        bonus2 = bonus2
    )
    try:
        if new_payroll:
            return jsonify({
                "code": "PAYROLL_CREATED",
                "message": f"Payroll {employee_id}, '{batch}' is created"
            })
        else:
            return jsonify({
                "CODE":"ERROR",
                "messsage":f"Payroll {employee_id}, '{batch}' is not created due to some error"
            })
    except Exception as error:
        print(f"error:{error}")
        return jsonify({
            "CODE":"EXCEPTIONAL_ERROR_OCCURED",
            "message":f"Exceptional error occured for payroll {employee_id}, '{batch}' creation, please try again"
        })