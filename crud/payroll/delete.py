from database import db
from models import Payroll
from sqlalchemy.exc import IntegrityError

#Delete payroll
def delete_payroll_crud(employee_id, batch):
    try:
        delete_query = Payroll.query.filter_by(employee_id=employee_id, batch=batch).first()
        db.session.delete(delete_query)
        db.session.commit()
    
        if delete_query:
            return delete_query
        else:
            return delete_query
        
    except IntegrityError:
        print("raising exception for integrity")
        raise

    except Exception:
        print("raising exception for unknown error")
        raise
