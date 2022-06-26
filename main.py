from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel): # o cara que define o DataType e validador de campos
    title: str
    content: str
    published: bool = True # valor padrão = true
    rating: Optional[int] = None # é optional, se não tiver = none

# variavel para salvar os posts em memoria
my_posts = [{
    "title": "title of post1", 
    "content": "content of post1", 
    "id": 1
    },
    {
    "title": "favorite foods", 
    "content": "I like pizza", 
    "id": 2
    }
]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/") #decorator > method: get, root path domain. ou seja é o caminho da url
def root(): # nome de cada função
    return {"message": "Hello World"} # o que acontece


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data": post_dict} # send o dicionario em json


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id) # tem que converter para str, pois a var é str
    return {"post_detail": post}
 
'''
# modelo sem o BaseModel
@app.post("/createposts")
def create_posts(payLoad: dict = Body(...)): # extradct all fields from body, convert to dict, store na variable payLoad
    print(payLoad)
    return {"new_post": f"title {payLoad['title']} content: {payLoad['content']}"}
# tittle str, content str  '''   

