from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from flask import g

#  Flask creates a new context every time a server request is made. 
# When the request ends, the context is removed from the app.
# These temporary contexts provide global variables, like the g object, 
# that can be shared across modules as long as the context is still active.

load_dotenv()

# connect to database using env variable
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def init_db(app):
  Base.metadata.create_all(engine)
  app.teardown_appcontext(close_db)
  # We're using the same Base.metadata.create_all() 
  # method from the seeds.py file, but we won't call 
  # it until after we've called init_db(), when the 
  # Flask app is ready

def get_db():
  # Whenever this function is called, it returns a new 
  # session-connection object. Other modules in the app 
  # can import Session directly from the db package, but 
  # using a function means that we can perform additional 
  # logic before creating the database connection.
  if 'db' not in g:
    # store db connection in app context
    g.db = Session()
  
  return g.db

def close_db(e=None):
  # pop() method attempts to find and remove db from the g object. 
  # If db exists (that is, db doesn't equal None), then db.close() 
  # will end the connection.
  db = g.pop('db', None)

  if db is not None:
    db.close()
