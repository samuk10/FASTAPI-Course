from pydantic import BaseModel, EmailStr
from datetime import datetime

# o cara que define o DataType e validador de campos
# schema/pydantic, define the structure of a request & response
class PostBase(BaseModel): 
    title: str
    content: str
    published: bool = True # valor padrão = true

class PostCreate(PostBase):
    pass

class Post(PostBase): # decide witch value returns
    id: int
    created_at: datetime

    # faz com que o pydantic "converta" o sql para dict, ler a doc.
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel): # return do client
    id: int
    email: EmailStr
    created_at: datetime

    # faz com que o pydantic "converta" o sql para dict, ler a doc.
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str