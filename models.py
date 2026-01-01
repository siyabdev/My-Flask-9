from database import db
from sqlalchemy import UniqueConstraint, CheckConstraint, Enum
from base import BaseModel
import enum

class RoleEnum(enum.Enum):
    admin = "admin"
    manager = "manager"
    guest = "guest"

class Employee(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    
    __table_args__ = (
        UniqueConstraint("email", name="unique_employee_email"),
        UniqueConstraint("username", name="unique_employee_username"),
        CheckConstraint("length(username) > 6", name="check_username_min_length"),
        CheckConstraint("length(password) > 8", name="check_password_min_length"),
    )
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "role": self.role
    }

    @classmethod
    def to_dict_list(cls, employees):
        return [emp.to_dict() for emp in employees]

class Payroll(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    batch = db.Column(db.Integer, nullable=False)
    basic_salary = db.Column(db.Integer, nullable = False)
    hourly_rate = db.Column(db.Integer, nullable=False)
    monthly_hours = db.Column(db.Integer, nullable = False)
    worked_hours = db.Column(db.Integer, nullable = False)
    early = db.Column(db.Integer, nullable = False)
    late = db.Column(db.Integer, nullable = False)
    leaves = db.Column(db.Integer, nullable = False) 
    bonus1 = db.Column(db.Integer, nullable = False)
    bonus2 = db.Column(db.Integer, nullable = False)

    __table_args__ = (
        UniqueConstraint("employee_id", "batch", name="unique_payroll_emp_batch"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "batch": self.batch,
            "basic_salary": self.basic_salary,
            "hourly_rate": self.hourly_rate,
            "monthly_hours": self.monthly_hours,
            "worked_hours": self.worked_hours,
            "early": self.early,
            "late": self.late,
            "leaves": self.leaves,
            "bonus1": self.bonus1,
            "bonus2": self.bonus2
        }
    
    @classmethod
    def to_dict_list(cls, payrolls):
        return [pay.to_dict() for pay in payrolls] 