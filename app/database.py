import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environmental variables from .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# PostgreSQL login details pulled from .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to database using login details
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create engine and base for models
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
