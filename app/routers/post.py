from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db

# router object removendo /posts
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
) 


'''#-- GET --#'''
@router.get("/", response_model=List[schemas.PostOut]) # transform into list
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
 limit: int = 10, skip: int = 0, search: Optional[str] = ""): # current_user forces user to be logged in to get post | "limit" query size
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    # OLDER filter_by search, limit of limit, skip 0 default
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    #results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        #models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
       models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    

# only sees own posts >  
#   posts = db.query(models.Post).filter(
#       models.Post.owner_id == current_user.id).all() # query posts from current logged user
    return posts # return json in the front

#-- CREATE --#
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # alterado para 201 ao criar
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # current_user forces user to be logged in to create post
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    # (post.title, post.content, post.published)) # não da pra passar o valor direto no insert
    #                 # NÃO USAR (f"INSERT etc...) perigo de sql injection
    # new_post = cursor.fetchone() # mostra o retorno do insert no sql
 
    # conn.commit()

    # enves de ter que digitar toda vez:
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    #print(current_user.id)
    #print(current_user.email)
    #usar para criar dict e retornar todos fields model
    new_post = models.Post(owner_id=current_user.id, **post.dict()) # owner_id is the user creating the post
    # dont forgot to add and commit
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # take what was add, put in a variable and return it

    return new_post # send the dictionary in json

#-- GET{ID} --#
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # current_user forces user to be logged in to get post # converter para int (para evitar inject)
    #cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),)) # convert str pois dá erro no SELECT
    #post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
       models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")

# if i wanted to only current user sees hes posts                            
#    if post.owner_id != current_user.id: # just post owner can delete post.
#        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                            detail="Not authorized to perform requested action")
        #response.status_code = status.HTTP_404_NOT_FOUND # forma feia
        #return {'message': f"Post with id: {id} was not found"}
    return post



#-- DELETE{ID} --# 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # current_user forces user to be logged in to delete post
    # deleting post
    # find the index in the array that has required ID
    # my_posts.pop(index)
    ## cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    ## deleted_post = cursor.fetchone()
    ## conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    
    # se não existir o id =
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id: # just post owner can delete post.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    # se existir o id = deletar ele.
    post_query.delete(synchronize_session=False)    
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    #return {'message': 'post was successfully deleted'}

#-- UPDATE{ID} --# 
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # current_user forces user to be logged in to update post

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

    if post.owner_id != current_user.id: # just post owner can delete post.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    # passar o dict com os valores a serem atualizados
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    # Replace specific spot in the array
    # se existir o id , pega o dado em guardado em post converte par dict

    return post_query.first()