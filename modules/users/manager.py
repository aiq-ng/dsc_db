from fastapi import HTTPException
from modules.shared.db import db
from modules.users.utils import validate_profile_data

class UserManager:
    async def get_profile(self, user_id: int):
        query = """
            SELECT up.*, u.email 
            FROM user_profiles up 
            JOIN users u ON u.id = up.user_id 
            WHERE up.user_id = $1
        """
        profile = await db.fetchrow(query, user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return profile

    async def create_profile(self, user_id: int, full_name: str, bio: str):
        if not validate_profile_data(full_name, bio):
            raise HTTPException(status_code=400, detail="Invalid profile data")
        
        query = """
            INSERT INTO user_profiles (user_id, full_name, bio) 
            VALUES ($1, $2, $3) 
            RETURNING *
        """
        return await db.fetchrow(query, user_id, full_name, bio)