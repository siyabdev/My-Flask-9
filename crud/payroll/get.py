from database import db
from utils.utils import get_payroll
from models import Payroll

#Get payroll
def get_payroll_crud(employee_id, batch):
    try:
        payroll = get_payroll(employee_id, batch)
        print (f"payroll:{payroll}")
        return payroll
    
    except Exception as error:
        print(f"error:{error}")
        return error

#Get all payrolls
def get_payrolls_crud():
    try:
        payrolls = Payroll.query.all()
        db.session.commit()
        print(f"All payrolls:{payrolls}")
        return payrolls
    except Exception as error:
        print(f"error:{error}")
        return error