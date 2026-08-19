from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from core.config import POSTGRESQL_DATABASE_URL

engine = create_engine(POSTGRESQL_DATABASE_URL)

LocalSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()