from flask import Blueprint, request, jsonify, current_app
from crud.payroll.get import get_payroll_crud, get_payrolls_crud
from schemas.payroll import PayrollResponse, PayrollListResponse
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
        current_app.logger.error("No id and batch.")
        return jsonify({
            "CODE":"NO_EMPLOYEE_ID_OR_BATCH_PROVIDED",
            "message":"Please enter employee id and batch"
        }), 403
    
    payroll = get_payroll_crud(employee_id=employee_id, batch=batch)

    print(f"employee:{payroll}")

    try:
        if payroll:
            return PayrollResponse(payroll).to_dict()
        
        else:
            current_app.logger.error("Id or batch doesnt exist")
            return jsonify({
                "CODE":"EMPLOYEE_ID_OR_BATCH_DOESNT_EXIST",
                "message": f"Please try another employee_id or batch, {employee_id}, '{batch}' is not registered"
            }), 403

    except Exception as error:
            print(f"error:{error}")
            current_app.logger.error("Exceptional error")
            return jsonify({
                "CODE":"EXCEPTIONAL_ERROR_OCCURED",
                "message":f"Exceptional error occured for getting payroll {employee_id} '{batch}', please try again"
            })
    
#Get all employees
@payroll_get_bp.route("/all", methods=["GET"])
@require_auth
def get_all_payrolls():
     
    try:
         get_payrolls = get_payrolls_crud()

         if get_payrolls:
              current_app.logger.info(f"All payrolls : {get_payrolls}")
              return PayrollListResponse.build(get_payrolls)
         else:
            current_app.logger.info("No payrolls found")
            return jsonify({
                "CODE":"NO_PAYROLLS_FOUND",
                "message":"No payrolls found, please add payroll first"
            })
    except Exception as error:
        print(f"error:{error}")
        current_app.logger.error("Exceptional error")
        return jsonify({
            "CODE":"EXCEPTIONAL_ERROR_OCCURED",
            "message":"Exceptional error occured for getting all payrolls, please try again"
        })


