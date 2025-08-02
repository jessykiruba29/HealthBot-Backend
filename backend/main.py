from fastapi import FastAPI
from ai_router import router as ai_router
from routes.r_form_router import form_router
import uvicorn


app=FastAPI()
app.include_router(ai_router)
app.include_router(form_router)

@app.get("/")
def home():
    return {"message": "Intelligent Patient Onboarding with Gemini"}
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
