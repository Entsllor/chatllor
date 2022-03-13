from fastapi import HTTPException, status

IncorrectLoginOrPassword = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"}
)

InvalidTokenPair = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Expected an active refresh token and an expired access token related to this user"
)

ExpectedActiveAccessToken = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Expected an active access token",
    headers={"WWW-Authenticate": "Bearer"},
)

CredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class ExpectedOneInstance(Exception):
    pass


class InstanceNotFound(Exception):
    pass
