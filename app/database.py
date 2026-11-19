from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
'''
import psycopg2
from psycopg2.extras import RealDictCursor
import time
'''

# Syntax to create a sqlalchemy db url
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<passward>@<ip-address/hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{settings.database_username}:"
    f"{settings.database_password}@"
    f"{settings.database_host}:"
    f"{settings.database_port}/"
    f"{settings.database_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, bind= engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# For connecting database to run sql commands. We don't need this when working with SQLAlchemy
'''
while True:
    try:
        conn = psycopg2.connect(host= 'localhost', database= 'fastapi', user= 'postgres', 
                                password= 'Tejas@123', cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("Connecting to database failed.")
        print("Error: ", error)
        time.sleep(2)
'''