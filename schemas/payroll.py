class CreatePayrollRequest:
    def __init__(self, data):
        self.employee_id = data.get("employee_id")
        self.batch = data.get("batch")
        self.basic_salary = data.get("basic_salary")
        self.hourly_rate = data.get("hourly_rate")
        self.monthly_hours = data.get("monthly_hours")
        self.worked_hours = data.get("worked_hours")
        self.early = data.get("early")
        self.late = data.get("late")
        self.leaves = data.get("leaves")
        self.bonus1 = data.get("bonus1")
        self.bonus2 = data.get("bonus2")

    def is_valid(self):
        if not all([self.employee_id, self.batch, self.basic_salary, self.hourly_rate, self.monthly_hours, self.worked_hours, self.early, self.late, self.leaves, self.bonus1, self.bonus2]):
            return False, "Missing required fields."
        
        if len(self.basic_salary) < 0:
            return False, "Basic salary should be greater than 0."
        if len(self.hourly_rate) < 0:
            return False, "Hourly rate should be greater than 0."
        if len(self.monthly_hours) < 0:
            return False, "Monthly hours should be greater than 0."
        if len(self.worked_hours) < 0:
            return False, "Worked hours should be greater than 0."
        
        return True, None

class UpdatePayrollRequest:
    def __init__(self, data):
        self.employee_id = data.get("employee_id")
        self.batch = data.get("batch")
        self.basic_salary = data.get("basic_salary")
        self.hourly_rate = data.get("hourly_rate")
        self.monthly_hours = data.get("monthly_hours")
        self.worked_hours = data.get("worked_hours")
        self.early = data.get("early")
        self.late = data.get("late")
        self.leaves = data.get("leaves")
        self.bonus1 = data.get("bonus1")
        self.bonus2 = data.get("bonus2")

    def is_valid(self):

        if not self.employee_id:
            return False, "Employee ID not provided."
        if not self.batch:
            return False, "Batch not provided."
             
        if len(self.basic_salary or self.hourly_rate or self.monthly_hours or self.worked_hours) < 0:
            return False, "Basic salary, hourly rate, monthly hours or worked hours should be greater than 0."
                
        return True, None
    
    def has_any_updates(self):
        return any([self.basic_salary, self.hourly_rate, self.monthly_hours, self.worked_hours, self.early, self.late, self.leaves, self.bonus1, self.bonus2])

class DeletePayrollRequest:
    def __init__(self, data):
        self.employee_id = data.get("employee_id")
        self.batch = data.get("batch")
    
    def is_valid(self):
        if not ([self.employee_id, self.batch]):
            return False, "No Employee ID and Batch provided."
        
        return True, None

class PayrollResponse:
    def __init__(self, payroll):
        self.id = payroll.id
        self.employee_id = payroll.employee_id
        self.batch = payroll.batch
        self.basic_salary = payroll.basic_salary
        self.hourly_rate = payroll.hourly_rate
        self.monthly_hours = payroll.monthly_hours
        self.worked_hours = payroll.worked_hours
        self.early = payroll.early
        self.late = payroll.late
        self.leaves = payroll.leaves
        self.bonus1 = payroll.bonus1
        self.bonus2 = payroll.bonus2

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

class PayrollListResponse:
    @staticmethod
    def from_list(payrolls):
        return [PayrollResponse(pay).to_dict() for pay in payrolls]
