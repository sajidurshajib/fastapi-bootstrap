import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

from app.services.config import config
from app.services.connection import sessionmanager

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.schemas.beanie_models import beanie_models

@asynccontextmanager
async def lifespan(app: FastAPI):
	#======================
	# PostgreSQL Connection
	#======================

	max_retries = 5
	retry_delay = 5  # seconds

	# Startup logic: Initialize and verify the database connection with retries
	sessionmanager.init(config.db_dsn)
	for attempt in range(max_retries):
		try:
			async with sessionmanager.session() as session:
				await session.execute(text('SELECT 1'))
				print(
					'[+] Database connection successfully established during startup.'
				)
			break
		except SQLAlchemyError as e:
			if attempt < max_retries - 1:
				print(
					f'[-] Failed to establish database connection (attempt {attempt + 1}/{max_retries}). Retrying in {retry_delay} seconds...'
				)
				await asyncio.sleep(retry_delay)
			else:
				print(
					'[-] Failed to establish database connection after several attempts.'
				)
				raise RuntimeError(
					'Database connection failed during startup. Exiting.'
				) from e
	
	# ==================
	# MongoDB Connection
	# ==================
	global mongo_client 
	mongo_client = AsyncIOMotorClient(config.mongo_dsn)

	try:
		await init_beanie(
			database=mongo_client[config.MONGODB_DATABASE],
			document_models=beanie_models,
			allow_index_dropping=True,
			recreate_views=True,
		)
		print('[+] MongoDB connection successfully established during startup.')
	except Exception as e:
		print(f'[-] MongoDB init failed: {e}')
		raise

	# separate startup and shutdown
	yield

	# Shutdown logic
	try:
		await sessionmanager.close()
		print('[/] Database connection closed during shutdown.')
	except Exception as e:
		print(f'[-] Error during shutdown: {e}')
