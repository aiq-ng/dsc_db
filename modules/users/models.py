from pydantic import BaseModel

class ProfileRequest(BaseModel):
    full_name: str
    bio: str