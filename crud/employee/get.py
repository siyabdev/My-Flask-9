from flask import current_app
from database import db
from utils.utils import get_employee
from models import Employee
from sqlalchemy.exc import IntegrityError

#Get employee
def get_employee_crud(username):
    try:
        employee = get_employee(username)
        print(f"employee:{employee}")
        return employee
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        return error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        return e

#Get all employees
def get_employees_crud():
    try:
        employees = Employee.query.all()
        db.session.commit()
        return employees

    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        return error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        return e

#Get short details (employee)
def get_employee_short_crud():
    try:
        employees = Employee.query.with_entities(Employee.id, Employee.name).all()
        db.session.commit()
        return employees
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e
