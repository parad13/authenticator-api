from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.orm import relationship
from db_pg.base_class import Base
from sqlalchemy.dialects.postgresql import ARRAY
import uuid
from sqlalchemy.dialects.postgresql import UUID


class ClientCredentials(Base):
    __tablename__ = "client_credentials"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(String)
    client_secret = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=None)
    updated_at = Column(DateTime, default=None)
    role = Column(ARRAY(String))
