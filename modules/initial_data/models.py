from pydantic import BaseModel, Field
from typing import Dict, Optional

# Operator Models
class OperatorBase(BaseModel):
    operator_name: str = Field(..., max_length=255)
    operator_code: str = Field(..., max_length=50)
    contact_info: Dict = Field(default_factory=dict)
    active: bool = True

class OperatorCreate(OperatorBase):
    pass

class OperatorUpdate(BaseModel):
    operator_name: Optional[str] = Field(None, max_length=255)
    operator_code: Optional[str] = Field(None, max_length=50)
    contact_info: Optional[Dict] = None
    active: Optional[bool] = None

class OperatorResponse(OperatorBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

# Offence Models
class OffenceBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None

class OffenceCreate(OffenceBase):
    pass

class OffenceUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None

class OffenceResponse(OffenceBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True