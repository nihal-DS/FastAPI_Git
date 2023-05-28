from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from app import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func


router = APIRouter(prefix = "/posts",
                   tags = ['Posts'])


# GET all posts
@router.get("/", response_model = List[schemas.PostOut])
def all_posts(db: Session = Depends(get_db),
               current_user: dict = Depends(oauth2.get_current_user),
               limit: int = 10,
               skip: int = 0,
               search: Optional[str] = ""):
    # postgres method
    # cursor.execute('''SELECT * FROM posts;''')
    # posts = cursor.fetchall()
    # Use ?limit=int in url to retrive limited number of posts
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results

# GET specific post 
@router.get("/{id}", response_model = schemas.PostOut)
def get_specific_post(id: int, db: Session = Depends(get_db),
                       current_user: dict = Depends(oauth2.get_current_user)):
    # cursor.execute('''SELECT * FROM posts WHERE id = %s''',(str(id)))
    # specific_post = cursor.fetchone()
    specific_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not specific_post:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT,
                            detail = f'Post with id : {id} not found')
    else:
        return specific_post

# POST request: create a post
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
def create_posts(payload: schemas.PostCreate, db: Session = Depends(get_db),
                  current_user: dict = Depends(oauth2.get_current_user)):
    # cursor.execute('''INSERT INTO posts (title, content, published)
    #                 VALUES (%s, %s, %s) RETURNING *''',
    #                 (payload.title, payload.content, payload.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id = current_user.id, **payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# DELETE request: delete a post
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                 current_user: dict = Depends(oauth2.get_current_user)):
    # cursor.execute('''DELETE FROM posts WHERE id = %s''', (str(id)))
    # deleted_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'Post with id: {id} does not exist')
    
    if int(post.owner_id) != int(current_user.id):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = 'Not authorized to do such action')

    post_query.delete(synchronize_session = False)
    db.commit()


# UPDATE request: update a post
@router.put("/{id}", response_model = schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: dict = Depends(oauth2.get_current_user)):
    # old_post = find_post(int(id))
    # if not old_post:
    #     raise HTTPException(status_code = status.HTTP_204_NO_CONTENT,
    #                         detail = 'Post you want to update does not exist')
    # else:
    #     idx = my_posts.index(old_post)
    #     my_posts[idx] = post
    # return {'action': 'Your post having id: {id} has been updated','current': my_posts}
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
         raise HTTPException(status_code = status.HTTP_204_NO_CONTENT,
                             detail = 'Post you want to update does not exist')
    
    if int(post.owner_id) != int(current_user.id):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = 'Not authorized to do such action')
    
    post_query.update(updated_post.dict(), synchronize_session = False)
    db.commit()
    return post_query.first()