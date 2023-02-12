from pydantic import BaseSettings, PostgresDsn


class PostgresSettings(BaseSettings):
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str

    class Config:
        env_file: str = ".env"

    @property
    def db_uri(self) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=self.DB_USERNAME,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            path=f"/{self.DB_NAME}",
        )
