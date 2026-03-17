from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"mysql+mysqlconnector://root:{os.getenv('DB_PASSWORD')}@localhost:3306/blog_api"

engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass

Session = sessionmaker(bind=engine)