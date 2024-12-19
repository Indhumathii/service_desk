from pydantic import BaseModel
from typing import Optional


class ServiceDeskCreate(BaseModel):
    title: str
    description: Optional[str]
    priority: str
    status: str


class ServiceDeskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
