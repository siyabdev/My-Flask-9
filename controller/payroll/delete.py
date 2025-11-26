from flask import Flask, Blueprint, request, jsonify
from crud.payroll.delete import delete_payroll_crud
from utils.utils import get_payroll
import logging
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

payroll_delete_bp = Blueprint("payroll_delete_bp", __name__, url_prefix="/payroll")

#Delete payroll
@payroll_delete_bp.route("/delete", methods=["DELETE"])
def delete_payroll():
    data = request.json
    employee_id = data.get("employee_id")
    batch = data.get("batch")

    if not employee_id or not batch:
        app.logger.error("Something required")
        return jsonify({"error": "Employee id and batch required"}), 400
    

    payroll = get_payroll(employee_id, batch)

    if not payroll:
        app.logger.info("Payroll doesnt exist.")
        return jsonify({
            "CODE": "PAYROLL_DOESNT_EXIST",
            "message": f"Payroll doesnt exist, please enter a valid employee id {employee_id} and batch '{batch}'"
        })
    try:
        delete_query = delete_payroll_crud(employee_id=employee_id, batch=batch)

    except IntegrityError as error:
        app.logger.error("Integrirty error")
        return jsonify({
            "CODE":"INTEGRITY_ERROR_OCCURED",
            "message":f"INTEGRITY error occured for payroll {employee_id}, '{batch}' deletion, {error}"
        })
    try:
        if delete_query:
                app.logger.info("Payroll deleted.")
                return jsonify({
                        "CODE": "PAYROLL_DELETED",
                        "message": f"Payroll {employee_id}, '{batch}' is deleted"
                    })
    except Exception as error:
            print(f"error:{error}")
            app.logger.error("Exceptional error")
            return jsonify({
                "CODE":"EXCEPTIONAL_ERROR_OCCURED",
                "message":f"Exceptional error occured for payroll {employee_id}, '{batch}' deletion, please try again"
            })

