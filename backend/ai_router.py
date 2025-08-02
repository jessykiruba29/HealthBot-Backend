from fastapi import APIRouter
from models import PatientInput
from gemini import j_get_guidance

router=APIRouter()

@router.post("/analyze")
async def analyze(data:PatientInput):
    guidance = j_get_guidance(data.symptoms)
    return {
        "name": data.name,
        "age": data.age,
        "gender": data.gender,
        "department": guidance["department"],
        "reason": guidance["reason"],
        "next_steps": guidance["next_steps"]
    }

