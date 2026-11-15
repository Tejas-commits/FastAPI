from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from app.routers import post, user, auth

models.Base.metadata.create_all(bind= engine)

app = FastAPI()

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

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "title of post 2", "content": "content of post 2", "id": 2}]

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get('/')
def root():
    return {"Message": "Hello World"}

@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'status': posts}

'''
@app.post('/posts')
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)        # Output the data in dict format
    return {"data": post_dict}
'''

'''
@app.get('/posts/{id}')
def get_post(id: int):         # For method 1 & 2, we gotta pass 'response: Response' as a parameter
    post = find_post(id)
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"Post with id: {id} was not found.")       # (Method 3)
        # response.status_code = 404       (Method 1)
        # response.status_code = status.HTTP_404_NOT_FOUND     (Method 2)
        # return {"Message": f"Post with id: {id} was not found."}
        
    print(post)
    return {"post_details": post}
'''

'''
@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"ID : {id} not found")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    print(post)
    return {"message": "updated post"}
'''

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
