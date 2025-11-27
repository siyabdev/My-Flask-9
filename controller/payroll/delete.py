from flask import Flask, Blueprint, request, jsonify
from crud.payroll.delete import delete_payroll_crud
from utils.utils import get_payroll
import logging
from sqlalchemy.exc import IntegrityError
from schemas.payroll import DeletePayrollRequest

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

payroll_delete_bp = Blueprint("payroll_delete_bp", __name__, url_prefix="/payroll")

#Delete payroll
@payroll_delete_bp.route("/delete", methods=["DELETE"])
def delete_payroll():
    data = DeletePayrollRequest(request.json)

    if not data.is_valid():
        return jsonify({"error": "Employee Id and Batch required"}), 400

    payroll = get_payroll(data.employee_id, data.batch)

    if not payroll:
        app.logger.info("Payroll doesnt exist.")
        return jsonify({
            "CODE": "PAYROLL_DOESNT_EXIST",
            "message": f"Payroll doesnt exist, please enter a valid employee id {data.employee_id} and batch '{data.batch}'"
        })
    try:
        delete_query = delete_payroll_crud(employee_id=data.employee_id, batch=data.batch)
        
        if delete_query:
                app.logger.info("Payroll deleted.")
                return jsonify({
                        "CODE": "PAYROLL_DELETED",
                        "message": f"Payroll {data.employee_id}, '{data.batch}' is deleted"
                    })
    except IntegrityError as error:
        return jsonify({
            "CODE": "INTEGRITY_ERROR",
            "message": str(error)
        }), 409
    
    except Exception:
        return jsonify({"CODE": "ERROR"}), 500
