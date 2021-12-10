from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os 
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_SERVICE = os.environ['DB_SERVICE']
DB_PORT = os.environ['DB_PORT']
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URL  ='postgresql://{0}:{1}@{2}:{3}/{4}'.format(
            DB_USER, DB_PASS, DB_SERVICE, DB_PORT, DB_NAME
    )

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()