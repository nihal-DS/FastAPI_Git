#Used to hash passwords
from passlib.context import CryptContext

pwd_context = CryptContext(schemes = ["bcrypt"])

# Used to hash a plane string
def hash(password: str):
    return pwd_context.hash(password)

# Used to verify if the hash of plane password is same as the existing hashed password
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
