from pydantic import BaseSettings


class FastapiSettings(BaseSettings):
    FASTAPI_SECRET: str
    FASTAPI_HASH_ALGORITHM: str
    FASTAPI_HASH_EXPIRATION: int
    DEBUG: str
    class Config:
        env_file: str = ".env"