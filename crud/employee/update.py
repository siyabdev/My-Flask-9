from database import db
from controller.employee.create import get_employee

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

    except Exception as error:
        print(f"error:{error}")
        return error