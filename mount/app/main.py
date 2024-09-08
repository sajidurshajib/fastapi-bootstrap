from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.todo import todo
from app.services.connection import sessionmanager
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from app.services.lifespan import lifespan

# Check lifespan for startup and shutdown DB connection
app = FastAPI(title="FastAPI Bootstrap", lifespan=lifespan)

# For cors origin
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["X-Requested-With", "Content-Type"],  
)

# Root API 
@app.get("/")
def read_root():
    return {"message": "Hello, Admin!"}


# All routes 
app.include_router(todo.router, prefix='/v1')


# Check db connection 
@app.get("/db-health")
async def health_check():
    async with sessionmanager.session() as session:
        try:
            await session.execute(text("SELECT 1"))
            return {"status": "success", "message": "Database connection is healthy"}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="Database connection failed")

