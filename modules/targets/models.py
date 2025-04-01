from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import date

class TargetBase(BaseModel):
    target_name: str = Field(..., max_length=255)
    file_number: str = Field(..., max_length=100)
    target_number: Optional[str] = Field(None, max_length=100)
    folder: Optional[str] = Field(None, max_length=255)
    offence_id: int
    operator_id: int
    type: str = Field(..., max_length=100)
    origin: Optional[str] = Field(None, max_length=255)
    target_date: date
    metadata: Dict = Field(default_factory=dict)
    flagged: bool = False
    threat_level: Optional[str] = Field(None, pattern="^(High|Medium|Low)$")  # New field

class TargetCreate(TargetBase):
    pass

class TargetUpdate(BaseModel):
    target_name: Optional[str] = Field(None, max_length=255)
    file_number: Optional[str] = Field(None, max_length=100)
    target_number: Optional[str] = Field(None, max_length=100)
    folder: Optional[str] = Field(None, max_length=255)
    offence_id: Optional[int] = None
    operator_id: Optional[int] = None
    type: Optional[str] = Field(None, max_length=100)
    origin: Optional[str] = Field(None, max_length=255)
    target_date: date
    metadata: Optional[Dict] = None
    flagged: Optional[bool] = None
    threat_level: Optional[str] = Field(None, pattern="^(High|Medium|Low)$")  # New field

class TargetResponse(TargetBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True