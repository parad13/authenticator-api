from typing import Union
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import UUID


class ClientCredentialsBase(BaseModel):
    client_id: Union[str, None] = None
    client_secret: Union[str, None] = None


class ClientCredentialsFetch(ClientCredentialsBase):
    # grant_type: Union[str, None] = None

    class Config:
        orm_mode = True


class ClientCredentialsCreate(ClientCredentialsBase):
    class Config:
        orm_mode = True
