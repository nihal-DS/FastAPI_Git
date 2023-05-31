from fastapi import FastAPI, Depends
from fastapi.params import Body
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth, vote
# import routers
from fastapi.middleware.cors import CORSMiddleware

#Used to create models
# models.Base.metadata.create_all(bind = engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
    )


my_posts = [{"id": 1, "title": "post1", "content": "content1"},
            {"id": 2, "title": "post2", "content": "content2"}]

def find_post(id):
    for p in my_posts:
        if p['id'] == int(id):
            return p


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# First GET request
@app.get("/")
def send():
    return {'message': 'Hello World'}

# Sqlalchemy GET test
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts