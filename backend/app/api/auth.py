from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta
from app.models.user import UserCreate, UserLogin, TokenResponse
from app.services.user import user_service
from app.auth.jwt import jwt_service
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=dict)
async def register(user: UserCreate):
    """Register new user"""
    # Check if user already exists
    if user_service.get_user_by_username(user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    if user_service.get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    # Create user
    new_user = user_service.create_user(
        username=user.username,
        email=user.email,
        password=user.password,
        full_name=user.full_name
    )
    
    return {
        "id": new_user["id"],
        "username": new_user["username"],
        "email": new_user["email"],
        "message": "User registered successfully"
    }

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """Login user"""
    user = user_service.get_user_by_username(credentials.username)
    
    if not user or not user_service.verify_password(user, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Create JWT token
    access_token_expires = timedelta(minutes=30)
    access_token = jwt_service.create_access_token(
        data={"sub": str(user["id"]), "username": user["username"], "role": "member"},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 30 * 60  # seconds
    }

@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """Logout user"""
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=dict)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    user = user_service.get_user(current_user["user_id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "full_name": user["full_name"],
        "is_active": user["is_active"],
        "created_at": user["created_at"]
    }
