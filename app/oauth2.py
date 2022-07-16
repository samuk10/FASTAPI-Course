from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=' login')
# 
# SECRET_KEY,
# ALGORITHM,
# EXPIRATION_TIMER

SECRET_KEY = "z9x8c4wq6e21rti9384p32m1n53m654hg8jgh28n465c4vb18d8745456"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy() # copia e cola em uma nova variavel

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # expire time
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # decode the jwt
        id: str = payload.get("user_id") # extract the id

        if id is None: # error if no id
            raise credentials_exception
        #validate if matches token schema, just to ensure all the data in the token is there
        token_data = schemas.TokenData(id=id) 
    except JWTError:
        raise credentials_exception
    
    return token_data

"""take the token from request, 
verify the token from verify_access_token, 
extract the id, 
fetch the user from db and we can attach the user to any path operation and perform any necessary logic"""
# any endpoint where user need to login to use it, we add the this dependency
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    # return the id from token
    token = verify_access_token(token, credentials_exception)

    # search in db for the token.id
    user = db.query(models.User).filter(models.User.id == token.id).first()

    # return the user
    return user

