from fastapi import HTTPException, status

CredentialsError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="Could not validate credentials"
)

InvalidToken = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="Invalid token"
)

IncorrectPassword = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="Incorrect password"
)

EmptyPayload = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Payload is empty."
)

NoUserFound = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User does not exist. Use endpoint /auth/register."
)

UserAlreadyExists = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Username already exists in the database. "\
        "We don't have password restoration yet. "\
        "Please authenticate or register with new credentials."
)

DBManipulationFailure = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Database manipulation failed."
)

ForbiddenAlias = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Forbidden alias: ensure that it 1) uses only alphanumeric characters, _ or -, "\
        "2) does not consist of numbers only; 3) is not \"shorten\" or \"search\""
)

UnavailableAlias = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Alias is already being used."
)

ForbiddenAction = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="It is forbedden to delete or change a tiny url that is not created by you."
)

NoURLFound = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="URL not found in the database."
)