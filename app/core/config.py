from pydantic import BaseConfig


class Settings(BaseConfig):
    SECRET_KEY: str = "JF*)@_psjf)(_#@-032-f[+@_oofjlfaldksn)dsf-)_*#)@H"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    DATABASE_URL: str = "sqlite:///./sqlite.db"

    class Config:
        env_file = ".env"

settings = Settings()