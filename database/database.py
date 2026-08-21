from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# from core.config import POSTGRESQL_DATABASE_URL

SQLITE_DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(SQLITE_DATABASE_URL, connect_args={"check_same_thread": False})

LocalSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()