from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/fastapi"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Responsible por criar/fechar as sessões com o db, todo request da API ela será chamada.
# add "db: Session = Depends(get_db) nas funções para que ela funcione.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

## connect to db without sqlalchemy
#import psycopg2 # driver do psql
#from psycopg2.extras import RealDictCursor # tras um dict com nome da coluna(psycopg2 tras errado)
#import time
#
## loop para tentar conectar ao banco, para em caso de erro o app não funfar sem
#while True:
#    try:
#        conn = psycopg2.connect(host='localhost', dbname='fastapi', user='postgres', 
#                                password='postgres', cursor_factory=RealDictCursor)
#        cursor = conn.cursor()
#        print("\nDatabase connection was successful!\n")
#        break
#    except Exception as error: # em caso de erro printar o error
#        print("\nConnecting to database failed\n")
#        print("Error: ", error)
#        time.sleep(3) # em caso de erro, esperar 3 sec para tentar novamente