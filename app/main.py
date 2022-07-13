from fastapi import FastAPI, status, HTTPException, Response, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List # é optional, se não tiver = none
from random import randrange
import psycopg2 # driver do psql
from psycopg2.extras import RealDictCursor # tras um dict com nome da coluna(psycopg2 tras errado)
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

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




'''#-- GET --#'''
@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts # return json in the front

#-- CREATE --#
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # alterado para 201 ao criar
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    # (post.title, post.content, post.published)) # não da pra passar o valor direto no insert
    #                 # NÃO USAR (f"INSERT etc...) perigo de sql injection
    # new_post = cursor.fetchone() # mostra o retorno do insert no sql
 
    # conn.commit()

    # enves de ter que digitar toda vez:
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)

    #usar para criar dict e retornar todos fields model
    new_post = models.Post(**post.dict())
    # não esquecer de add e comitar
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # pega o que foi adicionado, coloca na variável e retorna

    return new_post # send o dicionario em json

#-- GET{ID} --#
@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)): # converter para int (para eviter inject)
    #cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),)) # convert str pois dá erro no SELECT
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND # forma feia
        #return {'message': f"Post with id: {id} was not found"}
    return post



#-- DELETE{ID} --# 
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # deleting post
    # find the index in the array that has required ID
    # my_posts.pop(index)
    ## cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    ## deleted_post = cursor.fetchone()
    ## conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)
    
    # se não existir o id =
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} does not exist")
    # se existir o id = deletar ele.
    post.delete(synchronize_session=False)    
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    #return {'message': 'post was succesfully deleted'}

#-- UPDATE{ID} --# 
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):

    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #(post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()

    # procura um post
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # pega o primeiro
    post = post_query.first()

    # se não existir o id da 404
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} does not exist")

    # passar o dict com os valores a serem atualizados
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    # Replace specific spot in the array
    # se existir o id , pega o dado em guardado em post converte par dict

    return post_query.first()

'''
# modelo sem o BaseModel
@app.post("/createposts")
def create_posts(payLoad: dict = Body(...)): # extradct all fields from body, convert to dict, store na variable payLoad
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
    return {"data": "sucessfull"} # return sucessfull in the front
'''