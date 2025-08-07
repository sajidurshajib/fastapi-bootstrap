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
	MONGODB_HOST: str
	RABBITMQ_USER: str      
	RABBITMQ_PASS: str      
	RABBITMQ_HOST: str
	SECRET_KEY: str
	ALGORITHM: str

	@property
	def db_dsn(self) -> str:
		return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}'
	
	@property
	def mongo_dsn(self) -> str:
		return f"mongodb://{self.MONGODB_USER}:{self.MONGODB_PASS}@{self.MONGODB_HOST}:27017/{self.MONGODB_DATABASE}"

	@property
	def rabbit_dsn(self) -> str:
		return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASS}@{self.RABBITMQ_HOST}/"

	class Config:
		env_file = '.env'
		env_file_encoding = 'utf-8'


config = Config()
