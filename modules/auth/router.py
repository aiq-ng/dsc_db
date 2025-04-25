from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from modules.auth.manager import AuthManager
from modules.auth.utils import ALGORITHM, SECRET_KEY
from modules.shared.db import db

from .models import RegisterRequest

router = APIRouter()
auth_manager = AuthManager()

# Define the OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        query = "SELECT id, email FROM users WHERE email = $1"
        user = await db.fetchrow(query, email)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await auth_manager.login(form_data.username, form_data.password)


@router.post("/register/")
async def register(request: RegisterRequest):
    return await auth_manager.register(request.email, request.password)


@router.get("/me/")
async def get_current_user(current_user=Depends(get_current_user)):
    return {"current_user": current_user}
