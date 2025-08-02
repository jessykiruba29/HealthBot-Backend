from fastapi import FastAPI
from ai_router import router as ai_router

app=FastAPI()
app.include_router(ai_router)

@app.get("/")
def home():
    return {"message": "Intelligent Patient Onboarding with Gemini"}
