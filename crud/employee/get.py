from flask import current_app
from database import db
from utils.utils import get_employee
from models import Employee

#Get employee
def get_employee_crud(username):
    try:
        employee = get_employee(username)
        print(f"employee:{employee}")
        return employee
    
    except Exception as error:
        current_app.logger.error("Exceptional error")
        return error

#Get all employees
def get_employees_crud():
    try:
        employee = Employee.query.all()
        db.session.commit()
        print(f"employee all:{employee}")
        return employee
    except Exception as error:
        current_app.logger.error("Exceptional error")
        return error

#Get short details (employee)
def get_employee_short_crud(username):
    try:
        employee = get_employee(username)
        print(f"employee:{employee}")
        return employee
    
    except Exception as error:
        current_app.logger.error("Exceptional error")
        return error