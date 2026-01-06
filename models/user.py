from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))

    histories = relationship("History", back_populates="owner")