from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/fastapi"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Resposavel por criar/fechar as sessões com o db, todo request da API ela será chamada.
# add "db: Session = Depends(get_db) nas funções para que ela funcione.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()