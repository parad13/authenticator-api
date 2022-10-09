from typing import Optional

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.client_credentials import ClientCredentials
from schemas.client_credentials import (
    ClientCredentialsFetch,
    ClientCredentialsCreate,
)


class CRUDUsClientCredentials(
    CRUDBase[ClientCredentials, ClientCredentialsCreate, ClientCredentialsFetch]
):
    def get_client_credentials(
        self, db: Session, *, client_credentials: ClientCredentialsFetch
    ) -> Optional[ClientCredentials]:
        is_active = True
        client_cred = (
            db.query(ClientCredentials)
            .filter(
                ClientCredentials.client_id == client_credentials.client_id,
                ClientCredentials.is_active == is_active,
            )
            .first()
        )
        return client_cred


client_credentials = CRUDUsClientCredentials(ClientCredentials)
