from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= 'login')
# Anytime we have a specific endpoint that needs to be protected i.e. the user needs to be logged in to 
# use it, we add that dependency to the specific endpoint using our get_current_user function and expect 
# that they provide a access token and we verify with our function.

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_enocde = data.copy()

    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_enocde.update({"exp": expire})

    encoded_jwt = jwt.encode(to_enocde, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data

    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"Could not validate Creadentials",
                                          headers={"WWW-Authenicate": "Bearer"})

    return verify_access_token(token, credentials_exception)
