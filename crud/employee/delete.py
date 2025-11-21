from database import db
from controller.employee.create import get_employee
from models import Employee

#Delete employee
def delete_employee_crud(username):
    employee_by_username = get_employee(username)
    delete_query = False

    try:
        if employee_by_username:
            delete_query = Employee.query.filter_by(username=username).first()
            db.session.delete(delete_query)
            db.session.commit()
        
            if delete_query:
                return delete_query, employee_by_username
        else:
            return delete_query, employee_by_username
            
    except Exception as error:
        print(f"error:{error}")
        return error
    
    return {"message": "Employee deleted successfully"}, 200
