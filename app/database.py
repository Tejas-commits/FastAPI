from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Syntax to create a sqlalchemy db url
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<passward>@<ip-address/hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:Tejas%40123@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, bind= engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()