from fastapi import APIRouter, Depends
# from fastapi_jwt_auth import AuthJWT
# from core.auth_jwt import AuthJWT
from crud import revoke_crud
from fastapi_jwt_auth import AuthJWT

router = APIRouter()

@router.delete('/access-revoke')
def access_revoke(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    jti = Authorize.get_raw_jwt()['jti']
    revoke_crud.denylist.add(jti)
    print(revoke_crud.denylist)
    print("Token added to denylist")
    return {"detail":"Token has been revoked"}

@router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}
