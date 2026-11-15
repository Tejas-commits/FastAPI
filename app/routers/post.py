from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import engine, get_db

router = APIRouter(
    prefix= '/posts',
    tags= ['Posts']            # Helps to catagorize routes in fastapi swagger ui
)

@router.get('/', response_model= List[schemas.Post])
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute('''SELECT * FROM posts''')
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    return posts


@router.post('/', status_code= status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                 user_id: int = Depends(oauth2.get_current_user)):
    
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

    print(user_id)
    new_post = models.Post(**post.dict())   # (Method 2)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}')
def get_one_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
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



@router.delete('/{id}', status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                user_id: int = Depends(oauth2.get_current_user)):
    # index = find_index_post(id)

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"ID : {id} not found")

    post.delete(synchronize_session= False)
    db.commit()
    
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) 


@router.put('/{id}')
def update_post(id:int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                user_id: int = Depends(oauth2.get_current_user)):
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