# In this file, we implement the logic for login process using JWT token authentication

from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags= ['Authentication'])

@router.post('/login', response_model= schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}






# Notes:
'''
the OAuth2PasswordRequestForm stores the data into a dictionary consisting of:
{
    "username": "tejas"
    "password": "tejas@123"
}
It only checks the username and doesn't care to verify if its an id, email, or else.

In postman app, we can't send the data in 'raw json' format using a post request.
Here, we need to use the 'form-data' format to send the data.
'''