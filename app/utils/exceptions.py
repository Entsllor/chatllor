from fastapi import HTTPException, status

IncorrectLoginOrPassword = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"}
)

InvalidAuthTokens = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Expected an active refresh token and an access token with valid signature (allow expired)",
    headers={"WWW-Authenticate": "Bearer"}
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

InActiveUser = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Current user is inactive",
    headers={"WWW-Authenticate": "Bearer"},
)

UserNotFoundError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Failed to find this User",
    headers={"WWW-Authenticate": "Bearer"},
)

Forbidden = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Sorry, but you do not have enough rights",
    headers={"WWW-Authenticate": "Bearer"},
)


class ExpectedOneInstance(Exception):
    pass


class InstanceNotFound(Exception):
    pass
