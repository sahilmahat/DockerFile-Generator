from fastapi import FastAPI
app=FastAPI()
@app.get("/")
async def home():
    return{"message":"docker file generator running"}

@app.get("/health")
async def health_check():
    return{
        "status":"healthy",
        "service":"Dockerfile-genertor"
    }