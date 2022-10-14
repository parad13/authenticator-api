from fastapi_jwt_auth import AuthJWT


# A storage engine to save revoked tokens. in production,
# you can use Redis for storage system
# denylist = set()
denylist = set()
# print(denylist, "denylist1")

# For this example, we are just checking if the tokens jti
# (unique identifier) is in the denylist set. This could
# be made more complex, for example storing the token in Redis
# with the value true if revoked and false if not revoked
@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    # print(decrypted_token['jti'], "decrypted_token")
    # print(denylist, "denylist")
    jti = decrypted_token['jti']
    # print(jti, "jti")
    print(jti in denylist)
    # print(denylist)
    return jti in denylist

