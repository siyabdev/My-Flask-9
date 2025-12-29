from flask import Blueprint, request, jsonify, current_app
from crud.payroll.delete import delete_payroll_crud
from utils.utils import get_payroll
from sqlalchemy.exc import IntegrityError
from schemas.payroll import DeletePayrollRequest
from auth import require_auth

payroll_delete_bp = Blueprint("payroll_delete_bp", __name__, url_prefix="/payroll")

#Delete payroll
@payroll_delete_bp.route("/delete", methods=["DELETE"])
@require_auth
def delete_payroll():
    data = DeletePayrollRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error(f"Schema error {message}."), 400
        return jsonify({
            "code": "SCHEMA_ERROR",
            "message": f"Schema error occured {message}."
        }), 400

    payroll = get_payroll(data.employee_id, data.batch)

    if not payroll:
        current_app.logger.info(f"Payroll {payroll} doesnt exist.")
        return jsonify({
            "code": "PAYROLL_DOESNT_EXIST",
            "message": f"Payroll {payroll} doesnt exist, please enter a valid employee id {data.employee_id} and batch '{data.batch}'."
        })
    try:
        delete_query = delete_payroll_crud(employee_id=data.employee_id, batch=data.batch)
        if delete_query:
            current_app.logger.info(f"Payroll {payroll} deleted.")
            return jsonify({
                    "code": "PAYROLL_DELETED",
                    "message": f"Payroll {data.employee_id}, '{data.batch}' is deleted."
                })
    
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
