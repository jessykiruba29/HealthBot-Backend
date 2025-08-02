from pydantic import BaseModel
from typing import Optional

class PatientInput(BaseModel):
    name: Optional[str] = None
    symptoms: str
    age: Optional[int] = None
    gender: Optional[str] = None