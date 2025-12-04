from flask import current_app
from database import db
from utils.utils import get_employee
from sqlalchemy.exc import IntegrityError

#Update employee
def update_employee_crud(username, name, email, role, password):
    employee = get_employee(username)

    if not employee:
        return employee == False
    try:
        # Update any fields provided
        if name:
            employee.name = name
        
        if email:
            employee.email = email
        
        if role:
            employee.role = role
        
        if password:
            employee.password = password

        db.session.commit()

        print("inserted into database")

        return employee
    
    except IntegrityError:
        current_app.logger.error("raising exception for integrity")
        raise

    except Exception:
        current_app.logger.error("raising exception for unknown error")
        raise
