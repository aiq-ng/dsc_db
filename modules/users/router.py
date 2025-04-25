from fastapi import APIRouter, Depends

from modules.auth.router import get_current_user
from modules.users.manager import UserManager

from .models import ProfileRequest

router = APIRouter()
user_manager = UserManager()


@router.get("/profile/{user_id}/")
async def get_profile(user_id: int, current_user=Depends(get_current_user)):
    return await user_manager.get_profile(user_id)


@router.post("/profile/")
async def create_profile(
    request: ProfileRequest, current_user=Depends(get_current_user)
):
    # Assuming we can get user_id from current_user in a real scenario
    user_id = current_user["current_user"][
        0
    ]  # This would come from current_user in a complete implementation
    return await user_manager.create_profile(
        user_id, request.full_name, request.bio
    )
