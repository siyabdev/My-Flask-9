class CreateEmployeeRequest:
    def __init__(self, data):
        self.name = data.get("name")
        self.email = data.get("email")
        self.username = data.get("username")
        self.password = data.get("password")
        self.role = data.get("role", "guest")

    def is_valid(self):
        return all([self.name, self.email, self.username, self.password])

class UpdateEmployeeRequest:
    def __init__(self, data):
        self.username = data.get("username")
        self.name = data.get("name")
        self.email = data.get("email")
        self.password = data.get("password")
        self.role = data.get("role")

    def has_username(self):
        return self.username is not None

    def has_any_updates(self):
        return any([self.name, self.email, self.password, self.role])


class DeleteEmployeeRequest:
    def __init__(self, data):
        self.username = data.get("username")

    def is_valid(self):
        return self.username is not None


class EmployeeResponse:
    def __init__(self, employee):
        self.id = employee.id
        self.name = employee.name
        self.email = employee.email
        self.username = employee.username
        self.role = employee.role

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "username": self.username,
            "role": self.role
        }


class EmployeeListResponse:
    @staticmethod
    def build(employees):
        return [EmployeeResponse(emp).to_dict() for emp in employees]
