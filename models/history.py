from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import mapped_column, relationship
from database import Base

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = mapped_column(ForeignKey("user.id"))
    animale_name = Column(String(255))
    animale_rate_reconize = Column(Integer)
    date = Column(DateTime(timezone=True), server_default=func.now())
    uri = Column(String(255))

    owner = relationship("User", back_populates="histories")
