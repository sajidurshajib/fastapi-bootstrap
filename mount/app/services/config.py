from pydantic_settings import BaseSettings


class Config(BaseSettings):
	ENVIRONMENT: str
	DB_USER: str
	DB_PASSWORD: str
	DB_HOST: str
	DB_NAME: str
	MONGODB_USER: str
	MONGODB_PASS: str
	MONGODB_DATABASE: str
	SECRET_KEY: str
	ALGORITHM: str

	@property
	def db_dsn(self) -> str:
		return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}'
	
	@property
	def mongo_dsn(self) -> str:
		return f"mongodb://{self.MONGODB_USER}:{self.MONGODB_PASS}@localhost:27017"

	class Config:
		env_file = '.env'
		env_file_encoding = 'utf-8'


config = Config()
