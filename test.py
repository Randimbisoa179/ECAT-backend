# Dans un interpréteur Python, pas dans un fichier de l'application
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash("ben")
print(hashed_password)
  
