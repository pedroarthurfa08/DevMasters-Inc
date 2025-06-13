from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "DevMasters API"
    
    class Config:
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings() 