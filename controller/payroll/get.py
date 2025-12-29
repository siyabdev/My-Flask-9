from flask import Blueprint, request, jsonify, current_app
from crud.payroll.get import get_payroll_crud, get_payrolls_crud
from schemas.payroll import PayrollResponse, PayrollListResponse
from sqlalchemy.exc import IntegrityError
from auth import require_auth

payroll_get_bp = Blueprint("payroll_get_bp", __name__, url_prefix="/payroll")

#Get payroll
@payroll_get_bp.route("/get", methods=["GET"])
@require_auth
def get_payroll():
    data = request.json
    employee_id = data.get("employee_id")
    batch = data.get("batch")

    if not employee_id or not batch:
        current_app.logger.error(f"No employee id {employee_id} and batch {batch}.")
        return jsonify({
            "code":"NO_EMPLOYEE_ID_OR_BATCH_PROVIDED",
            "message":f"Please enter employee id {employee_id} and batch {batch}."
        }), 403
    
    payroll = get_payroll_crud(employee_id=employee_id, batch=batch)

    try:
        if payroll:
            current_app.logger.info(f"Payroll {payroll} response returned.")
            return PayrollResponse(payroll).to_dict()
        
        else:
            current_app.logger.error(f"Employee id {employee_id} or batch {batch} doesnt exist.")
            return jsonify({
                "code":"EMPLOYEE_ID_OR_BATCH_DOESNT_EXIST",
                "message": f"Please try another employee_id or batch, {employee_id}, '{batch}' not registered"
            }), 403
        
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
    
#Get all payrolls
@payroll_get_bp.route("/all", methods=["GET"])
@require_auth
def get_all_payrolls():
     
    try:
         get_payrolls = get_payrolls_crud()

         if get_payrolls:
              current_app.logger.info(f"All payrolls {get_payrolls} response returned.")
              return PayrollListResponse.from_list(get_payrolls)
         else:
            current_app.logger.info(f"No payrolls {get_payrolls} found.")
            return jsonify({
                "code":"NO_PAYROLLS_FOUND",
                "message":f"No payrolls {get_payrolls} found, please add any payroll first."
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