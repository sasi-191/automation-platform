from sqlalchemy import Column, Integer, String
from database import Base

class RuleTable(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    current_price = Column(Integer)
    target_price = Column(Integer)
    message = Column(String(150))
    action = Column(String(100))

class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    hashed_password = Column(String(255))