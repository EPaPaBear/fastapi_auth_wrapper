# import statements
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get the properties from environment variables
load_dotenv(r"resources/.env")

# Create a database engine & connect to database
DbEngine = create_engine(os.getenv("DATABASE_URL"))

# Create a database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=DbEngine
)

Base = declarative_base()