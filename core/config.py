import os
from dotenv import load_dotenv

load_dotenv()

POSTGRESQL_DATABASE_URL=os.getenv("POSTGRESQL_DATABASE_URL")
JWT_SECRET=os.getenv("JWT_SECRET")
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION=int(os.getenv("JWT_EXPIRATION", 600))