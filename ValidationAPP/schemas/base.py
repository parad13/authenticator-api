from pydantic import BaseModel


class TestEcho(BaseModel):
    message: str
