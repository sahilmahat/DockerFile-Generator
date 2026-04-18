from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name:str="Dockerfile Generator"
    debug:bool= True
    groq_api_key: str=" "
    github_client_id:str=" "
    github_client_secret:str=" "

    class Config:
        env_file= ".env"
settings= Settings()