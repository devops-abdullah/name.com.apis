"""Services module"""
from .namecom import namecom_service
from .domain import domain_service
from .dns import dns_service
from .team import team_service
from .user import user_service

__all__ = [
    "namecom_service",
    "domain_service",
    "dns_service",
    "team_service",
    "user_service",
]
