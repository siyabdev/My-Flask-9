from database import db
from models import Employee

#Create employee
def create_employee_crud(name, email, username, password, role):

    try:
        create_query = Employee(
            name=name,
            email=email,
            username=username,
            password=password,
            role=role
        )
        
        db.session.add(create_query)
        db.session.commit()
        
        return create_query
    
    except Exception as error:
        print(f"error:{error}")
        return error
