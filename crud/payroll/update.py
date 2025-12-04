from flask import current_app
from database import db
from utils.utils import get_payroll
from sqlalchemy.exc import IntegrityError

#Update payroll
def update_payroll_crud(employee_id, batch, basic_salary, hourly_rate, monthly_hours, worked_hours, early, late, leaves, bonus1, bonus2):
    payroll = get_payroll(employee_id, batch)

    if not payroll:
        return payroll == False
    try:
        # Update any fields provided
        if basic_salary:
            payroll.basic_salary = basic_salary
        
        if hourly_rate:
            payroll.hourly_rate = hourly_rate
        
        if monthly_hours:
            payroll.monthly_hours = monthly_hours
        
        if worked_hours:
            payroll.worked_hours = worked_hours
        
        if early:
            payroll.early = early
        
        if late:
            payroll.late = late
        
        if leaves:
            payroll.leaves = leaves

        if bonus1:
            payroll.bonus1 = bonus1

        if bonus2:
            payroll.bonus2 = bonus2

        db.session.commit()

        print("inserted into database")

        return payroll

    except IntegrityError:
        current_app.logger.error("raising exception for integrity")
        raise

    except Exception:
        current_app.logger.error("raising exception for unknown error")
        raise