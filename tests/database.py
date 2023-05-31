from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.database import get_db
from app.database import Base
import pytest

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