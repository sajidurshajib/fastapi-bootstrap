from sqlalchemy import Column, String, Integer, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel


class Role(BaseModel):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(50), nullable=False, unique=True)
    permissions = Column(JSON, nullable=True)

    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role(id={self.id}, role='{self.role}')>"
