from database import db
from models import Employee
from sqlalchemy.exc import IntegrityError

#Delete employee
def delete_employee_crud(username):
    try:
        delete_query = Employee.query.filter_by(username=username).first()
        db.session.delete(delete_query)
        db.session.commit()
        return delete_query
    
    except IntegrityError:
        print("raising exception for integrity")
        raise
    
    except Exception:
        print("raising exception for unknown error")
        raise
