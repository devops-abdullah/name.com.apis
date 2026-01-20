from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DNSRecord(BaseModel):
    id: Optional[int] = None
    domain: str
    name: str
    type: str
    content: str
    ttl: Optional[int] = 3600
    priority: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Domain(BaseModel):
    id: Optional[int] = None
    name: str
    namecom_id: Optional[str] = None
    team_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class DomainWithRecords(Domain):
    records: List[DNSRecord] = []

class CreateDNSRecord(BaseModel):
    name: str
    type: str
    content: str
    ttl: Optional[int] = 3600
    priority: Optional[int] = None

class UpdateDNSRecord(BaseModel):
    content: Optional[str] = None
    ttl: Optional[int] = None
    priority: Optional[int] = None
