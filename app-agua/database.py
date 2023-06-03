from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

database_name = config['DEFAULT']['DB_NAME']
database_password = config['DEFAULT']['DB_PASSWORD']
database_user = config['DEFAULT']['DB_USER']
IP = config['DEFAULT']['IP']
PORT = config['DEFAULT']['PORT']

SQLALCHEMY_DATABASE_URL = {url_database}
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, #connect_args={"check_same_thread": False}
    #connect_args es oly for sqlite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
