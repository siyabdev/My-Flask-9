from flask import Blueprint, request, jsonify, current_app
from crud.payroll.delete import delete_payroll_crud
from utils.utils import get_payroll
from sqlalchemy.exc import IntegrityError
from schemas.payroll import DeletePayrollRequest

payroll_delete_bp = Blueprint("payroll_delete_bp", __name__, url_prefix="/payroll")

#Delete payroll
@payroll_delete_bp.route("/delete", methods=["DELETE"])
def delete_payroll():
    data = DeletePayrollRequest(request.json)
    valid, message = data.is_valid

    if not valid:
        current_app.logger.error({"error": f"Schema error. {message}"}), 400
        return jsonify({"error": f"Schema error. {message}"}), 400

    payroll = get_payroll(data.employee_id, data.batch)

    if not payroll:
        current_app.logger.info("Payroll doesnt exist.")
        return jsonify({
            "CODE": "PAYROLL_DOESNT_EXIST",
            "message": f"Payroll doesnt exist, please enter a valid employee id {data.employee_id} and batch '{data.batch}'"
        })
    try:
        delete_query = delete_payroll_crud(employee_id=data.employee_id, batch=data.batch)
        
        if delete_query:
                current_app.logger.info("Payroll deleted.")
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
