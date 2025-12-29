from models import Employee
from models import Payroll

def get_employee(username):
    employee = Employee.query.filter_by(username=username).first()
    return employee

def get_payroll(employee_id, batch):
    payroll = Payroll.query.filter_by(employee_id=employee_id, batch=batch).first()
    return payroll