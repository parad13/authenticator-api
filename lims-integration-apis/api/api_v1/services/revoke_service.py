from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

router = APIRouter()

@router.delete('/access-revoke')
def access_revoke(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    jti = Authorize.get_raw_jwt()['jti']
    revoke_crud.denylist.add(jti)
    return {"detail":"Access token has been revoke"}