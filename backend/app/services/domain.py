from typing import Optional, List
from datetime import datetime

class DomainService:
    """Service for managing domains"""
    
    def __init__(self):
        self.domains = {}  # In-memory storage for demo, replace with DB
        self.counter = 1
    
    def create_domain(self, name: str, team_id: int, namecom_id: Optional[str] = None):
        """Create domain record"""
        domain = {
            "id": self.counter,
            "name": name,
            "namecom_id": namecom_id,
            "team_id": team_id,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        self.domains[self.counter] = domain
        self.counter += 1
        return domain
    
    def get_domain(self, domain_id: int):
        """Get domain by ID"""
        return self.domains.get(domain_id)
    
    def get_team_domains(self, team_id: int) -> List:
        """Get all domains for a team"""
        return [d for d in self.domains.values() if d["team_id"] == team_id]
    
    def update_domain(self, domain_id: int, name: Optional[str] = None):
        """Update domain"""
        if domain_id in self.domains:
            if name:
                self.domains[domain_id]["name"] = name
            self.domains[domain_id]["updated_at"] = datetime.now()
            return self.domains[domain_id]
        return None
    
    def delete_domain(self, domain_id: int):
        """Delete domain"""
        if domain_id in self.domains:
            del self.domains[domain_id]
            return True
        return False

domain_service = DomainService()
