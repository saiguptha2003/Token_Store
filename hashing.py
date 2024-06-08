
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def getPasswordHashed(password):
    return pwd_context.hash(password)

def getVerified(password,hashedPassword):
    return pwd_context.verify(password,hashedPassword)

