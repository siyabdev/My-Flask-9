from database import db

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="guest")

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

class Payroll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    batch = db.Column(db.String(20), nullable=False)
    basic_salary = db.Column(db.Integer, nullable = False)
    hourly_rate = db.Column(db.Integer, nullable=False)
    monthly_hours = db.Column(db.Integer, nullable = False)
    worked_hours = db.Column(db.Integer, nullable = False)
    early = db.Column(db.Integer, nullable = False)
    late = db.Column(db.Integer, nullable = False)
    leaves = db.Column(db.Integer, nullable = False) 
    bonus1 = db.Column(db.Integer, nullable = False)
    bonus2 = db.Column(db.Integer, nullable = False)

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