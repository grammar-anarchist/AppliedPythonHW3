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
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User does not exist. Use endpoint /auth/register."
)

UserAlreadyExists = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Username already exists in the database. "\
        "We don't have password restoration yet. "\
        "Please authenticate or register with new credentials."
)

DBModificationFailure = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Database modification failed."
)
