from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from starlette import status

router = APIRouter(tags=["auth"])

security = HTTPBasic()

# Dummy database of users
users_db = {
    "user1": "password1",
    "user2": "password2",
}


class User(BaseModel):
    username: str
    password: str


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    if username not in users_db or users_db[username] != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return username


@router.post("/login")
def login(credentials: HTTPBasicCredentials = Depends(security)):
    username = authenticate_user(credentials)
    return {"message": f"Welcome {username}"}


@router.get("/secure-data")
def read_secure_data(credentials: HTTPBasicCredentials = Depends(security)):
    username = authenticate_user(credentials)
    return {"message": f"Secure data for {username}"}
