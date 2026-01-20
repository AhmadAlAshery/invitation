from sqlalchemy import Column, Integer, String
from src.core.model import ORMBase


class User(ORMBase):
    __tablename__ = "users"

    
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
