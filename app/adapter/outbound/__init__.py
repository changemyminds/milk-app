from app.config.env_config import env_config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(env_config.get_db_connection())
Base = declarative_base()
