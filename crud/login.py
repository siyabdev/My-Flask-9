from models import Employee

def verify_login(username, password):
    """
    Check if username and password match an employee in the database
    Returns the employee if login is successful, None if failed
    """
    # Find employee by username
    employee = Employee.query.filter_by(username=username).first()
    
    # If employee not found, return None
    if not employee:
        return None
    
    # Check if password matches (simple comparison for basic implementation)
    # Note: In production, passwords should be hashed!
    if employee.password == password:
        return employee
    
    # Password doesn't match
    return None

