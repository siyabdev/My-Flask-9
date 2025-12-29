from flask import current_app
from database import db
from utils.utils import get_payroll
from models import Payroll
from sqlalchemy.exc import IntegrityError

#Get payroll
def get_payroll_crud(employee_id, batch):
    try:
        payroll = get_payroll(employee_id, batch)
        return payroll
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        return error

    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        return e


#Get all payrolls
def get_payrolls_crud():
    try:
        payrolls = Payroll.query.all()
        db.session.commit()
        return payrolls
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error

    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e
