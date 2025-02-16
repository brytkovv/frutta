from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    message = Column(String(4096), nullable=True)
    can_change = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Answer(key={self.key}, can_change={self.can_change})>"
