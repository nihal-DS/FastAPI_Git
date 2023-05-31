from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.database import get_db
from app.database import Base
import pytest
from app.oauth2 import create_access_token
from app import models

# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:gabon2u@localhost:5432/fastapi_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Engine is responsible to connect to the database

#To talk to the database we use session
TestingSessionLocal = sessionmaker(autocommit = False,
                            autoflush = False,
                            bind = engine)

# Base.metadata.create_all(bind = engine)

# Create base class(returns a class)
# Base = declarative_base() 

# Used to initiate a session and then close it out
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture 
def session():
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user2(client):
    user_data = {"email": "high@gmail.com",
                 "password": "xdd"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user(client):
    user_data = {"email": "high1@gmail.com",
                 "password": "xddx"}
    res = client.post("/users/", json = user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {"title": "1st_title",
         "content": "1st_content",
         "owner_id": test_user['id']},
        {"title": "2nd_title",
         "content": "2nd_content",
         "owner_id": test_user['id']},
        {"title": "3rd_title",
         "content": "3rd_content",
         "owner_id": test_user2['id']}
    ]

    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, posts_data)
    post_list = list(post_map)
    
    session.add_all(post_list)
    session.commit()
    posts = session.query(models.Post).all()
    return posts