from app.db.session import SessionLocal
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = SessionLocal()

hashed = pwd_context.hash("testpass")
user = User(username="lucas", hashed_password=hashed, role="admin")

db.add(user)
db.commit()
print("Created test user")
