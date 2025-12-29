import enum

class RoleType(enum.Enum):
    admin = 'admin'
    manager = 'manager'
    guest = 'guest'

class CreateEmployeeRequest:
    def __init__(self, data):
        self.name = data.get("name")
        self.email = data.get("email")
        self.username = data.get("username")
        self.password = data.get("password")
        self.role = data.get("role", "guest")

    def is_valid(self):
        # Required fields
        if not all([self.name, self.email, self.username, self.password, self.role]):
            return False, "Missing required fields."

        # Validate username length
        if len(self.username) < 6:
            return False, "Username must be at least 6 characters long."

        # Validate password length
        if len(self.password) < 6:
            return False, "Password must be at least 6 characters long."

        # Validate role against enum
        if self.role not in [role.value for role in RoleType]:
            return False, "Invalid role provided."

        return True, None

class UpdateEmployeeRequest:
    def __init__(self, data):
        self.username = data.get("username")
        self.name = data.get("name")
        self.email = data.get("email")
        self.password = data.get("password")
        self.role = data.get("role")

    def is_valid(self):

        if not self.username:
            return False, "Username not provided."

        # Validate username length
        if len(self.username) < 6:
            return False, "Username must be at least 6 characters long."

        # Validate password length
        if len(self.password) < 6:
            return False, "Password must be at least 6 characters long."

        # Validate role against enum
        if self.role and self.role not in [role.value for role in RoleType]:
            return False, "Invalid role provided."
        
        return True, None

    def has_any_updates(self):
        return any([self.name, self.email, self.password, self.role])

class DeleteEmployeeRequest:
    def __init__(self, data):
        self.username = data.get("username")

    def is_valid(self):
        if not ([self.username]):
            return False, "No username."
        
        return True, None
    
class EmployeeResponse:
    def __init__(self, employee):
        self.id = employee.id
        self.name = employee.name
        self.email = employee.email
        self.username = employee.username
        self.password = employee.password
        self.role = employee.role.value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "role": self.role
        }

class EmployeeShortResponse:
    def __init__(self, employee):
        self.id= employee.id
        self.name = employee.name
    
    def to_dict(self):
        return{
            "id" : self.id,
            "name" : self.name
        }
    @staticmethod
    def from_list(employees):
        return [EmployeeShortResponse(emp).to_dict() for emp in employees]
        
class EmployeeListResponse:
    @staticmethod
    def from_list(employees):
        return [EmployeeResponse(emp).to_dict() for emp in employees]