from pydantic import BaseModel
from datetime import date
from typing import Optional, Dict


# Pydantic Models
class TargetBase(BaseModel):
    target_name: str
    number: str
    folder: Optional[str] = None
    offence_id: int
    operator_id: int
    type: str
    origin: Optional[str] = None
    target_date: date
    metadata: Optional[Dict] = {}

class TargetCreate(TargetBase):
    pass

class TargetUpdate(BaseModel):
    target_name: Optional[str] = None
    number: Optional[str] = None
    folder: Optional[str] = None
    offence_id: Optional[int] = None
    operator_id: Optional[int] = None
    type: Optional[str] = None
    origin: Optional[str] = None
    target_date: Optional[date] = None
    metadata: Optional[Dict] = None

class TargetResponse(TargetBase):
    id: int
    created_at: str
    updated_at: str
