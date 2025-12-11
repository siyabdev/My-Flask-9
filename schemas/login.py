class LoginRequest:
    def __init__(self, data):
        self.username = data.get("username")
        self.password = data.get("password")
    
    def is_valid(self):
        if not self.username:
            return False, "Username is required"
        
        if not self.password:
            return False, "Password is required"
        
        return True, None

class LoginResponse:
    def __init__(self, token, user_id, username):
        self.token = token
        self.user_id = user_id
        self.username = username
    
    def to_dict(self):
        return {
            "token": self.token,
            "user_id": self.user_id,
            "username": self.username
        }

