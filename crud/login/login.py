from flask import current_app
from models import Employee

def verify_login(username, password):
    employee = Employee.query.filter_by(username=username).first()
    
    if not employee:
        current_app.logger.info(f"No employee {employee }.")
        return None
    
    if employee.password == password:
        current_app.logger.info(f"Employee {employee} returned.")
        return employee
    
    return None

