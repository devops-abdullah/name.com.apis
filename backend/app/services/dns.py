from typing import Optional
from datetime import datetime

class DNSService:
    """Service for managing DNS records"""
    
    def __init__(self):
        self.records = {}  # In-memory storage for demo
        self.counter = 1
    
    def create_record(
        self,
        domain_id: int,
        domain_name: str,
        name: str,
        type: str,
        content: str,
        ttl: int = 3600,
        priority: Optional[int] = None
    ):
        """Create DNS record"""
        record = {
            "id": self.counter,
            "domain_id": domain_id,
            "domain_name": domain_name,
            "name": name,
            "type": type,
            "content": content,
            "ttl": ttl,
            "priority": priority,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        self.records[self.counter] = record
        self.counter += 1
        return record
    
    def get_record(self, record_id: int):
        """Get record by ID"""
        return self.records.get(record_id)
    
    def get_domain_records(self, domain_id: int) -> list:
        """Get all records for a domain"""
        return [r for r in self.records.values() if r["domain_id"] == domain_id]
    
    def update_record(
        self,
        record_id: int,
        content: Optional[str] = None,
        ttl: Optional[int] = None,
        priority: Optional[int] = None
    ):
        """Update DNS record"""
        if record_id in self.records:
            if content:
                self.records[record_id]["content"] = content
            if ttl:
                self.records[record_id]["ttl"] = ttl
            if priority is not None:
                self.records[record_id]["priority"] = priority
            self.records[record_id]["updated_at"] = datetime.now()
            return self.records[record_id]
        return None
    
    def delete_record(self, record_id: int):
        """Delete DNS record"""
        if record_id in self.records:
            del self.records[record_id]
            return True
        return False

dns_service = DNSService()
