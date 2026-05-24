from pydantic import BaseModel


class Settings(BaseModel):

    MAX_CONCURRENT_JOBS: int = 3


settings = Settings()
