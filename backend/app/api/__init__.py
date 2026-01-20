"""API Routes"""
from .auth import router as auth_router
from .teams import router as teams_router
from .domains import router as domains_router

__all__ = ["auth_router", "teams_router", "domains_router"]
