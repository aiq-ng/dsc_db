from pydantic import BaseModel, Field
from typing import Optional

class SuggestionBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = Field(None, max_length=1000)

class SuggestionCreate(SuggestionBase):
    pass

class SuggestionResponse(SuggestionBase):
    id: int
    user_id: int
    created_at: str

    class Config:
        from_attributes = True