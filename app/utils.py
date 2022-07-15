from passlib.context import CryptContext


"""
# jwt token auth doesn't store data on api/database
# client login, api check pw and return
# /posts{token} # uses token in payload
# /api checks everytime if token is valid
# its not encrypted,
# header, payload and verify sing
"""
# whe user login, pw comes plain, we hash it and compare with database!

# hash algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# func to makes easy to use
def hash(password: str):
    return pwd_context.hash(password)

# takes plain pw, hash and compare with hashed in db
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)