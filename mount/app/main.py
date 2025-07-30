from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

from app.api.dashboard import router as dashboard_router
from app.api.v1 import router as v1_router
from app.services.connection import sessionmanager
from app.services.exceptions import (
	catch_exceptions_middleware,
	general_exception_handler,
	http_exception_handler,
	validation_exception_handler,
)
from app.services.lifespan import lifespan
from app.utils.logger import LogAPIMiddleware, Logger
from app.services.config import config



# Check lifespan for startup and shutdown DB connection
app = FastAPI(
	title='FastAPI Bootstrap', 
	lifespan=lifespan, 
	docs_url='/docs' if config.ENVIRONMENT == 'dev' else None, 
	redoc_url=None
	)


# init logger
logger = Logger(__name__)


# For cors origin
origins = [
	'http://localhost:3000',
]

app.add_middleware(LogAPIMiddleware)
app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=['*'],
	allow_headers=['X-Requested-With', 'Content-Type'],
)

# Register exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Add middleware
app.middleware('http')(catch_exceptions_middleware)


# Root API
@app.get('/')
async def health_check():
	async with sessionmanager.session() as session:
		try:
			await session.execute(text('SELECT 1'))
			logger.info('Database connection is healthy')
			return {
				'status': 'success',
				'message': 'Database connection is healthy',
			}
		except SQLAlchemyError as e:
			logger.error(e)
			raise HTTPException(
				status_code=500, detail='Database connection failed'
			)


# All routes
app.include_router(v1_router, prefix='/api/v1')
app.include_router(dashboard_router, prefix='/api/dashboard')
