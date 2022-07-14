from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

# router object removendo /posts
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
) 


'''#-- GET --#'''
@router.get("/", response_model=List[schemas.Post]) # transform into list
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts # return json in the front

#-- CREATE --#
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # alterado para 201 ao criar
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

    return new_post # send o dictionary em json

#-- GET{ID} --#
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)): # converter para int (para evitar inject)
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
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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
    #return {'message': 'post was successfully deleted'}

#-- UPDATE{ID} --# 
@router.put("/{id}", response_model=schemas.Post)
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