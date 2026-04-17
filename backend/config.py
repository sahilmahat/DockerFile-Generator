from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name:str="Dockerfile Generator"
    debug:bool= True
    antropic_api_key: str=" "
    github_client_key:str=" "
    github_client_secret:str=" "

    class Config:
        env_file= ".env"
settings= Settings()