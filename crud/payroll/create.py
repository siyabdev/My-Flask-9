from database import db
from models import Payroll

#Create payroll
def create_payroll_crud(employee_id, batch, basic_salary, hourly_rate, monthly_hours, worked_hours, early, late, leaves, bonus1, bonus2):

    print("payroll call recieved")

    try:
        create_query = Payroll(
            employee_id = employee_id,
            batch = batch,
            basic_salary = basic_salary,
            hourly_rate = hourly_rate,
            monthly_hours = monthly_hours,
            worked_hours = worked_hours,
            early = early,
            late = late,
            leaves = leaves,
            bonus1 = bonus1,
            bonus2 = bonus2
        )
        
        db.session.add(create_query)
        db.session.commit()
        
        return create_query
    
    except Exception as error:
        print(f"error:{error}")
        return error
