from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import BaseModel


class Profile(BaseModel):
	__tablename__ = 'profiles'

	id = Column(Integer, primary_key=True, index=True)
	address = Column(String, nullable=True)
	secondary_address = Column(String, nullable=True)
	phone = Column(String, nullable=True)
	secondary_phone = Column(String, nullable=True)
	dob = Column(Date, nullable=True)
	sex = Column(String, nullable=True)

	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

	user = relationship('User', back_populates='profile')

	def __repr__(self):
		return f'<Profile(id={self.id})>'
