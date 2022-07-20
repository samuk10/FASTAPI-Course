from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# o cara que define o DataType e validador de campos
# schema/pydantic, define the structure of a request & response
class PostBase(BaseModel): 
    title: str
    content: str
    published: bool = True # valor padrão = true

class PostCreate(PostBase):
    pass

class UserOut(BaseModel): # return do client
    id: int
    email: EmailStr
    created_at: datetime

    # faz com que o pydantic "converta" o sql para dict, ler a doc.
    class Config:
        orm_mode = True

class Post(PostBase): # decide witch value returns
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut # return UserOut(the info of the user)

    # faz com que o pydantic "converta" o sql para dict, ler a doc.
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None