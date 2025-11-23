from database import db
from utils.utils import get_payroll
from models import Payroll

#Delete payroll
def delete_payroll_crud(employee_id, batch):
    payroll = get_payroll(employee_id, batch)
    delete_query = False

    try:
        if payroll:
            delete_query = Payroll.query.filter_by(employee_id=employee_id, batch=batch).first()
            db.session.delete(delete_query)
            db.session.commit()
        
            if delete_query:
                return delete_query, payroll
        else:
            return delete_query, payroll
            
    except Exception as error:
        print(f"error:{error}")
        return error
    
    return {"message": "Payroll deleted successfully"}, 200