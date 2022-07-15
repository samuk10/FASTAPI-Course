from jose import JWTError, jwt
from datetime import datetime, timedelta

# 
# SECRET_KEY,
# ALGORITHM,
# EXPIRATION_TIMER

SECRET_KEY = "z9x8c4wq6e21rti9384p32m1n53m654hg8jgh28n465c4vb18d8745456"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy() # copia e cola em uma nova variavel

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # expire time
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


