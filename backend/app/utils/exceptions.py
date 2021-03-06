from fastapi import HTTPException, status
from fastapi.exception_handlers import http_exception_handler


class BaseAppException(Exception):
    as_http: HTTPException


async def app_exception_handler(request, exc: BaseAppException):
    return await http_exception_handler(request, exc.as_http)


class IncorrectLoginOrPassword(BaseAppException):
    as_http = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )


class ExpectedActiveAccessToken(BaseAppException):
    as_http = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Expected an active access token",
        headers={"WWW-Authenticate": "Bearer"},
    )


class CredentialsException(BaseAppException):
    as_http = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


class InActiveUser(BaseAppException):
    as_http = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Current user is inactive",
        headers={"WWW-Authenticate": "Bearer"},
    )


class UserNotFoundError(BaseAppException):
    as_http = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Failed to find this User",
        headers={"WWW-Authenticate": "Bearer"},
    )


class Forbidden(BaseAppException):
    as_http = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Sorry, but you do not have enough rights",
        headers={"WWW-Authenticate": "Bearer"},
    )


class ExpectedOneInstance(BaseAppException):
    as_http = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="There are duplicates that cannot be processed"
    )


class InstanceNotFound(BaseAppException):
    as_http = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Failed to find this object"
    )


class ExpectedUniqueUsername(BaseAppException):
    as_http = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Username is already taken",
    )
