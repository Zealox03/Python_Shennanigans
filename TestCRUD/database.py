from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'mysql+pymysql://root:admin_123@localhost:3306/BlogApplication'

# This is to declare the connection to database
# create_engine: Creates the database engine using your connection string (URL_DATABASE)
# sessionmaker: session factory bounds to your engine
# declarative_base: Provide a base class for your ORM Models
engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


