from pydantic import BaseModel


class Client(BaseModel):
    client_id: str
    client_secret: str
    role: list[str]

    class Config:
        orm_mode = True
