from flask import current_app
from database import db
from models import Employee
from sqlalchemy.exc import IntegrityError

#Create employee
def create_employee_crud(name, email, username, password, role):

    print("calling employee crud")

    try:
        create_query = Employee(
            name=name,
            email=email,
            username=username,
            password=password,
            role=role
        )

        print("attempting database insert")
        
        db.session.add(create_query)

        print("attempting commit")

        db.session.commit()

        print("commit complete")

        return create_query

    except IntegrityError:
        current_app.logger.error("raising exception for integrity")
        raise
    
    
    except Exception:
        current_app.logger.error("raising exception for unknown error")
        raise
