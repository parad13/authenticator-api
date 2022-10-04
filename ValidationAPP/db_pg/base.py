# Import all the models, so that Base has them before being
# imported by Alembic
from db_pg.base_class import Base  # noqa
from models import report_model, client_credentials
