from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DocumentCreate(BaseModel):
    title: str
    description: str
    tag: str

class DocumentResponse(BaseModel):
    id: int
    title: str
    description: str
    tag: str
    created_at:datetime

    class Config:
        from_attributes= True
        
class DocumentVersionResponse(BaseModel):
    id: int
    version: int
    created_at: datetime

    class Config:
        from_attributes = True

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tag: Optional[str] = None  
