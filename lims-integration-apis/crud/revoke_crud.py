from fastapi_jwt_auth import AuthJWT


denylist = set()
print(denylist, "denylist")


@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token["jti"]
    return jti in denylist
