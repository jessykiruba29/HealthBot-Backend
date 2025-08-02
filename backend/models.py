from pydantic import BaseModel

class PatientInput(BaseModel):
    name: str
    symptoms: str
    age: int | None = None
    gender: str | None = None