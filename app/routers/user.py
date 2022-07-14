from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db


# router object removendo /posts
router = APIRouter(
    prefix="/users",
    tags=['Users']
) # router object

#/** response_model= , vai fazer com que o user receba apenas os valores explicitos.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut) 
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # hash the password and store in user.password 
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict()) # takes user, convert to dict and unpack
    # não esquecer de add e comitar
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # pega o que foi adicionado, coloca na variável e retorna

    return new_user

# know if you are logged or not, and get a new token
# retrieve info from some user
@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} does not found")
                        
    return user
