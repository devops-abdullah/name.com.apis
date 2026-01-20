from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.models.team import Team, TeamCreate, TeamUpdate, TeamDetail
from app.services.team import team_service
from app.services.user import user_service
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/api/teams", tags=["teams"])

@router.post("", response_model=Team)
async def create_team(team: TeamCreate, current_user: dict = Depends(get_current_user)):
    """Create new team"""
    new_team = team_service.create_team(
        name=team.name,
        owner_id=current_user["user_id"],
        description=team.description
    )
    
    return {
        "id": new_team["id"],
        "name": new_team["name"],
        "description": new_team["description"],
        "owner_id": new_team["owner_id"],
        "created_at": new_team["created_at"]
    }

@router.get("", response_model=List[Team])
async def get_user_teams(current_user: dict = Depends(get_current_user)):
    """Get all teams for current user"""
    teams = team_service.get_user_teams(current_user["user_id"])
    return teams

@router.get("/{team_id}", response_model=TeamDetail)
async def get_team(team_id: int, current_user: dict = Depends(get_current_user)):
    """Get team details"""
    team = team_service.get_team(team_id)
    
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    members = team_service.get_team_members(team_id)
    
    return {
        "id": team["id"],
        "name": team["name"],
        "description": team["description"],
        "owner_id": team["owner_id"],
        "created_at": team["created_at"],
        "members": members,
        "member_count": len(members)
    }

@router.put("/{team_id}", response_model=Team)
async def update_team(team_id: int, team_update: TeamUpdate, current_user: dict = Depends(get_current_user)):
    """Update team"""
    team = team_service.get_team(team_id)
    
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    if team["owner_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only team owner can update team"
        )
    
    updated_team = team_service.update_team(
        team_id,
        name=team_update.name,
        description=team_update.description
    )
    
    return updated_team

@router.delete("/{team_id}")
async def delete_team(team_id: int, current_user: dict = Depends(get_current_user)):
    """Delete team"""
    team = team_service.get_team(team_id)
    
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    if team["owner_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only team owner can delete team"
        )
    
    team_service.delete_team(team_id)
    return {"message": "Team deleted successfully"}

@router.post("/{team_id}/members/{user_id}")
async def add_team_member(team_id: int, user_id: int, role: str = "member", current_user: dict = Depends(get_current_user)):
    """Add member to team"""
    team = team_service.get_team(team_id)
    
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    if team["owner_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only team owner can add members"
        )
    
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    member = team_service.add_member(team_id, user_id, role)
    return {"message": "Member added successfully", "member": member}

@router.delete("/{team_id}/members/{user_id}")
async def remove_team_member(team_id: int, user_id: int, current_user: dict = Depends(get_current_user)):
    """Remove member from team"""
    team = team_service.get_team(team_id)
    
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    if team["owner_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only team owner can remove members"
        )
    
    team_service.remove_member(team_id, user_id)
    return {"message": "Member removed successfully"}
