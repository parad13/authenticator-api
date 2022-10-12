from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT

class User(BaseModel):
    username: str
    password: str

# set denylist enabled to True
# you can set to check access or refresh token or even both of them
class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access","refresh"}

@AuthJWT.load_config
def get_config():
    return Settings()