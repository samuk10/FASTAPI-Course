from fastapi import FastAPI

from . import models
from .database import engine
from .routers import post, user, auth


# o cara que identifica e cria as tabelas no db, 
# mas, não modifica se houver uma tabela com o mesmo nome.
# usar "Alembic" caso for necessário alterar a estrutura das tabelas
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# importing the routes from post.router
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

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