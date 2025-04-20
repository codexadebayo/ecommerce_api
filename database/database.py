from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional, Generator
from core.config import settings  # Import the settings instance

#  Get the database URL from the settings
SQLALCHEMY_DATABASE_URL: str = settings.SQLALCHEMY_DATABASE_URL

#  Use create_engine, passing the URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#  Create a SessionLocal class.  Instances of this class will be
#  database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#  Create a Base class.  This is used for defining the database models.
#  See https://docs.sqlalchemy.org/en/14/orm/declarative_base.html
Base = declarative_base()

#  Dependency to get a database session.  This is used in FastAPI
#  route handlers.
def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get a database session.

    Yields:
        Session: A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    #  This code is only executed if you run this file directly
    #  (e.g., `python database/database.py`).  It's useful for
    #  testing the database connection.
    try:
        #  Create a session
        db = SessionLocal()
        #  Perform a simple query to test the connection.
        #  If the connection is successful, this should not raise an exception.
        db.execute("SELECT 1")
        print("Database connection successful!")
    except Exception as e:
        print("Error connecting to database:", e)
    finally:
        #  Close the session
        db.close()
