from fastapi import FastAPI, status, HTTPException, Response, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List # é optional, se não tiver = none
from random import randrange
import psycopg2 # driver do psql
from psycopg2.extras import RealDictCursor # tras um dict com nome da coluna(psycopg2 tras errado)
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user


# o cara que identifica e cria as tabelas no db, 
# mas, não modifica se houver uma tabela com o mesmo nome.
# usar "Alembic" caso for necessário alterar a estrutura das tabelas
models.Base.metadata.create_all(bind=engine)

app = FastAPI()



# loop para tentar conectar ao banco, para em caso de erro o app não funfar sem
while True:
    try:
        conn = psycopg2.connect(host='localhost', dbname='fastapi', user='postgres', 
                                password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("\nDatabase connection was successful!\n")
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

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts): # interate in the array and get index
        if p['id'] == id: # 
            return i # retorna o index no dictionary com o id specific

# importing the routes from post.router
app.include_router(post.router)
app.include_router(user.router)


@app.get("/") #decorator > method: get, root path domain. ou seja é o caminho da url
def root(): # nome de cada função
    return {"message": "Hello World"} # o que acontece






'''
# modelo sem o BaseModel
@app.post("/createposts")
def create_posts(payLoad: dict = Body(...)): # extract all fields from body, convert to dict, store na variable payLoad
    print(payLoad)
    return {"new_post": f"title {payLoad['title']} content: {payLoad['content']}"}
# tittle str, content str  '''   

'''TEST
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    # this way i get just data in frontend
    #posts = db.query(models.Post).all()
    #return {"data": posts}
    # this way i get the return and the select it made in sql
    posts = db.query(models.Post).all()
    print(posts)
    return {"data": "successful"} # return successful in the front
'''