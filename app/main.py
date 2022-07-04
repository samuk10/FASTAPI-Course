from fastapi import FastAPI, status, HTTPException, Response, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional # é optional, se não tiver = none
from random import randrange
import psycopg2 # driver do psql
from psycopg2.extras import RealDictCursor # tras um dict com nome da coluna(psycopg2 tras errado)
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel): # o cara que define o DataType e validador de campos
    title: str
    content: str
    published: bool = True # valor padrão = true

# loop para tentar conectar ao banco, para em caso de erro o app não funfar sem
while True:
    try:
        conn = psycopg2.connect(host='localhost', dbname='fastapi', user='postgres', 
                                password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("\nDatabase connection was sucessfull!\n")
        break
    except Exception as error: # em caso de erro printar o error
        print("\nConnecting to database failed\n")
        print("Error: ", error)
        time.sleep(3) # em caso de erro, esperar 3 sec para tentar novamente

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

#-- TEST --#
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "sucess"}

#-- GET --#
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

#-- CREATE --#
@app.post("/posts", status_code=status.HTTP_201_CREATED) # alterado para 201 ao criar
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    (post.title, post.content, post.published)) # não da pra passar o valor direto no insert
                    # NÃO USAR (f"INSERT etc...) perigo de sql injection
    new_post = cursor.fetchone() # mostra o retorno do insert no sql

    conn.commit()

    return {"data": new_post} # send o dicionario em json

#-- GET{ID} --#
@app.get("/posts/{id}")
def get_post(id: int): # converter para int (para eviter inject)
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),)) # convert str pois dá erro no SELECT
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND # forma feia
        #return {'message': f"Post with id: {id} was not found"}
    return {"post_detail": post}

#-- DELETE{ID} --# 
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # find the index in the array that has required ID
    # my_posts.pop(index)
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    # se não existir o id =
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    #return {'message': 'post was succesfully deleted'}

#-- UPDATE{ID} --# 
@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    (post.title, post.content, post.published, str(id)))

    updated_post = cursor.fetchone()
    conn.commit()

    # se não existir o id =
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} does not exist")

    # Replace specific spot in the array
    # se existir o id , pega o dado em guardado em post converte par dict

    return {'data': updated_post}

'''
# modelo sem o BaseModel
@app.post("/createposts")
def create_posts(payLoad: dict = Body(...)): # extradct all fields from body, convert to dict, store na variable payLoad
    print(payLoad)
    return {"new_post": f"title {payLoad['title']} content: {payLoad['content']}"}
# tittle str, content str  '''   

