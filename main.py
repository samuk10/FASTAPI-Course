from typing import Optional
from fastapi import FastAPI, status, HTTPException, Response
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

def find_index_post(id):
    for i, p in enumerate(my_posts): # interate in the array and get index
        if p['id'] == id: # 
            return i # retorna o index no dicionario com o id especifico

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


@app.post("/posts", status_code=status.HTTP_201_CREATED) # alterado para 201 ao criar
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data": post_dict} # send o dicionario em json


@app.get("/posts/{id}")
def get_post(id: int):
    
    post = find_post(id) # tem que converter para str, pois a var é str
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND # forma feia
        #return {'message': f"Post with id: {id} was not found"}
    return {"post_detail": post}
 
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # find the index in the array that has required ID
    # my_posts.pop(index)
    index = find_index_post(id)

    # se não existir o id =
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} does not exist")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    #return {'message': 'post was succesfully deleted'}

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    # se não existir o id =
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} does not exist")

    # Replace specific spot in the array
    # se existir o id , pega o dado em guardado em post converte par dict
    post_dict = post.dict()
    post_dict['id'] = id # descobriu a id no dict
    my_posts[index] = post_dict # nesse post com a index, replace with post_dict
    return {'data': "updated post"}

'''
# modelo sem o BaseModel
@app.post("/createposts")
def create_posts(payLoad: dict = Body(...)): # extradct all fields from body, convert to dict, store na variable payLoad
    print(payLoad)
    return {"new_post": f"title {payLoad['title']} content: {payLoad['content']}"}
# tittle str, content str  '''   

