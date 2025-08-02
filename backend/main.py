from fastapi import FastAPI
from ai_router import router as ai_router
from routes.r_form_router import form_router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
app.include_router(ai_router)
app.include_router(form_router)
# Allow requests from frontend (e.g., React running on localhost:3000)
origins = [
    "http://localhost:5173",  # React dev server
    "http://127.0.0.1:3000",  # Alternative localhost
    "*"  # ⚠️ Use only during development — allows all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],            # Allows all HTTP methods: POST, GET, etc.
    allow_headers=["*"],            # Allows all headers
)



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
