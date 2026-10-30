from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

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

@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute('''SELECT * FROM posts''')
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    return posts


@app.post('/posts', status_code= status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    #using sql
    '''
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    '''

    # using sqlachemy ORM 

    # new_post = models.Post(title= post.title, content= post.content, published= post.published)
    # This method is inefficient way of posting a new post as if he no. of attributes were like 50-100, we have to type all of them.

    print(post.dict())
    new_post = models.Post(**post.dict())   # (Method 2)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get('/posts/{id}')
def get_one_post(id: int, db: Session = Depends(get_db)):
    # using sql
    '''
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    '''

    # using sqlalchemy ORM
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} was not found.")

    return {"post_detail": post}


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

@app.delete('/posts/{id}', status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # index = find_index_post(id)

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"ID : {id} not found")

    post.delete(synchronize_session= False)
    db.commit()
    
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) 


@app.put('/posts/{id}')
def update_post(id:int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # using sql
    """
    cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''', 
                   (post.title, post.content, post.published, str(id)))
    
    updated_post = cursor.fetchone()
    conn.commit()
    """

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail= f"ID : {id} not found")

    post_query.update(updated_post.dict(), synchronize_session= False)
    db.commit()

    return {'data': post_query.first()}
