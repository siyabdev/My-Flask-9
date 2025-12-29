from flask import current_app
from database import db
from models import Employee
from sqlalchemy.exc import IntegrityError

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

    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e
