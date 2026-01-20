from typing import Optional, List
from datetime import datetime

class TeamService:
    """Service for managing teams"""
    
    def __init__(self):
        self.teams = {}
        self.members = {}  # team_id -> [user_ids]
        self.counter = 1
        self.member_counter = 1
    
    def create_team(self, name: str, owner_id: int, description: Optional[str] = None):
        """Create team"""
        team = {
            "id": self.counter,
            "name": name,
            "description": description,
            "owner_id": owner_id,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        self.teams[self.counter] = team
        self.members[self.counter] = [
            {
                "member_id": self.member_counter,
                "user_id": owner_id,
                "role": "admin",
                "joined_at": datetime.now()
            }
        ]
        self.member_counter += 1
        self.counter += 1
        return team
    
    def get_team(self, team_id: int):
        """Get team by ID"""
        return self.teams.get(team_id)
    
    def get_user_teams(self, user_id: int) -> List:
        """Get all teams for a user"""
        user_teams = []
        for team_id, members in self.members.items():
            if any(m["user_id"] == user_id for m in members):
                user_teams.append(self.teams[team_id])
        return user_teams
    
    def add_member(self, team_id: int, user_id: int, role: str = "member"):
        """Add member to team"""
        if team_id in self.teams and team_id in self.members:
            member = {
                "member_id": self.member_counter,
                "user_id": user_id,
                "role": role,
                "joined_at": datetime.now()
            }
            self.members[team_id].append(member)
            self.member_counter += 1
            return member
        return None
    
    def get_team_members(self, team_id: int) -> List:
        """Get all members of a team"""
        return self.members.get(team_id, [])
    
    def update_member_role(self, team_id: int, user_id: int, role: str):
        """Update member role"""
        if team_id in self.members:
            for member in self.members[team_id]:
                if member["user_id"] == user_id:
                    member["role"] = role
                    return member
        return None
    
    def remove_member(self, team_id: int, user_id: int):
        """Remove member from team"""
        if team_id in self.members:
            self.members[team_id] = [
                m for m in self.members[team_id] if m["user_id"] != user_id
            ]
            return True
        return False
    
    def update_team(self, team_id: int, name: Optional[str] = None, description: Optional[str] = None):
        """Update team"""
        if team_id in self.teams:
            if name:
                self.teams[team_id]["name"] = name
            if description:
                self.teams[team_id]["description"] = description
            self.teams[team_id]["updated_at"] = datetime.now()
            return self.teams[team_id]
        return None
    
    def delete_team(self, team_id: int):
        """Delete team"""
        if team_id in self.teams:
            del self.teams[team_id]
            if team_id in self.members:
                del self.members[team_id]
            return True
        return False

team_service = TeamService()
