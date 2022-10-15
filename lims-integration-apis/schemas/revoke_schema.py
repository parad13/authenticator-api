from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT

class Settings(BaseModel):
    authjwt_secret_key: str = "8c36c022e46a13ee44dd6d8711b9cc403f56e897ba268680913453a2021fcbb8"
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access","refresh"}

@AuthJWT.load_config
def get_config():
    return Settings()

