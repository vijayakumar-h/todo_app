from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DBTask(Base):
    __tablename__="tasks"
    id= Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    is_complete = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)


