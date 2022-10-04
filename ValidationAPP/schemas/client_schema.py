from pydantic import BaseModel
from typing import List

class Client(BaseModel):
    client_id: str
    client_secret: str
    role: List[str]

    class Config:
        orm_mode = True
