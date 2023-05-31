from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Engine is responsible to connect to the database

#To talk to the database we use session
SessionLocal = sessionmaker(autocommit = False,
                            autoflush = False,
                            bind = engine)

# Create base class(returns a class)
Base = declarative_base() 

# Used to initiate a session and then close it out
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Trying to establish a connection with database
# while True:
    # try:
    #     conn = psycopg2.connect(host = 'localhost', database = 'fastapi',
    #                             user = 'postgres', password = 'gabon2u',
    #                             cursor_factory = RealDictCursor)
    #     cursor = conn.cursor()
    #     print('Database connection was successfull!')
    #     break

    # except Exception as error:
    #     print('Connection to database failed')
    #     print('Error:', error)
    #     time.sleep(2)