from typing import Optional
from datetime import datetime
import hashlib

class UserService:
    """Service for managing users"""
    
    def __init__(self):
        self.users = {}
        self.counter = 1
    
    def create_user(self, username: str, email: str, password: str, full_name: Optional[str] = None):
        """Create user"""
        user = {
            "id": self.counter,
            "username": username,
            "email": email,
            "password": self._hash_password(password),
            "full_name": full_name,
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        self.users[self.counter] = user
        self.counter += 1
        return user
    
    def get_user(self, user_id: int):
        """Get user by ID"""
        return self.users.get(user_id)
    
    def get_user_by_username(self, username: str):
        """Get user by username"""
        for user in self.users.values():
            if user["username"] == username:
                return user
        return None
    
    def get_user_by_email(self, email: str):
        """Get user by email"""
        for user in self.users.values():
            if user["email"] == email:
                return user
        return None
    
    def verify_password(self, user: dict, password: str) -> bool:
        """Verify password"""
        return user["password"] == self._hash_password(password)
    
    def _hash_password(self, password: str) -> str:
        """Hash password"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def update_user(self, user_id: int, **kwargs):
        """Update user"""
        if user_id in self.users:
            for key, value in kwargs.items():
                if key != "password" and value is not None:
                    self.users[user_id][key] = value
            if "password" in kwargs and kwargs["password"]:
                self.users[user_id]["password"] = self._hash_password(kwargs["password"])
            self.users[user_id]["updated_at"] = datetime.now()
            return self.users[user_id]
        return None
    
    def deactivate_user(self, user_id: int):
        """Deactivate user"""
        if user_id in self.users:
            self.users[user_id]["is_active"] = False
            return self.users[user_id]
        return None

user_service = UserService()
