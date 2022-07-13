from pydantic import BaseModel
from datetime import datetime

# o cara que define o DataType e validador de campos
# schema/pydantic, define the structure of a request & response
class PostBase(BaseModel): 
    title: str
    content: str
    published: bool = True # valor padrão = true

class PostCreate(PostBase):
    pass

class Post(PostBase): # decide wich value returns
    id: int
    created_at: datetime

    # faz com que o pydantic "converta" o sql para dict, ler a doc.
    class Config:
        orm_mode = True