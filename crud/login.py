from models import Employee

def verify_login(username, password):
    employee = Employee.query.filter_by(username=username).first()
    
    if not employee:
        return None
    
    if employee.password == password:
        return employee
    
    return None

