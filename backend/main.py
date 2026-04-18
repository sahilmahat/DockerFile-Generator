from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.generate import router as generate_router
from routes.auth import router as auth_router


app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
        "https://dockerfile-generator.vercel.app"
        ],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate_router, prefix="/api")
app.include_router(auth_router, prefix="/api/auth")


@app.get("/")
async def home():
    return{"message":"docker file generator running"}

@app.get("/health")
async def health_check():
    return{
        "status":"healthy",
        "service":"Dockerfile-genertor"
    }