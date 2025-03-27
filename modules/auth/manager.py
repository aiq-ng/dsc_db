from fastapi import HTTPException, status
from modules.shared.db import db
from modules.auth.utils import verify_password, create_access_token, get_password_hash
from typing import Optional

class AuthManager:
    async def login(self, email: str, password: str) -> dict:
        query = "SELECT * FROM users WHERE email = $1"
        user = await db.fetchrow(query, email)
        
        if not user or not verify_password(password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        access_token = create_access_token(data={"sub": user["email"]})
        return {"access_token": access_token, "token_type": "bearer"}

    async def register(self, email: str, password: str) -> dict:
        hashed_password = get_password_hash(password)
        query = "INSERT INTO users (email, password) VALUES ($1, $2) RETURNING id, email"
        
        try:
            user = await db.fetchrow(query, email, hashed_password)
            access_token = create_access_token(data={"sub": user["email"]})
            return {"access_token": access_token, "token_type": "bearer"}
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )