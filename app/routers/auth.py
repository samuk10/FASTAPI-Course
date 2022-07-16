from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token) # make sure we return just the specified fields from "schemas.Token"
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    # OAuth2PasswordRequestForm, store two fields:
    #"""
    #
    #    "username": "asd", # NOT EMAIL!!!
    #     "password": "asd"
    #
    #"""
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # check login:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    # check pw:
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token
    # return token

    access_token = oauth2.create_access_token(data = {"user_id": user.id}) # field on the url token
    return {"access_token": access_token, "token_type": "bearer"}