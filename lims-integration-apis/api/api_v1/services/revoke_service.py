from fastapi import APIRouter, Depends, HTTPException, status
from crud import revoke_crud
from fastapi_jwt_auth import AuthJWT
import fastapi_jwt_auth

router = APIRouter()

@router.delete('/access-revoke')
def access_revoke(Authorize: AuthJWT = Depends()):
    try:

        Authorize.jwt_required()

        jti = Authorize.get_raw_jwt()['jti']
        revoke_crud.denylist.add(jti)
        return {"detail":"Token has been revoked"}
    

    except fastapi_jwt_auth.exceptions.RevokedTokenError:
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Token has been revoked",
    )
