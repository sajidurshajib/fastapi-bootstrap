from fastapi import Depends, status
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.connection import get_db
from app.usecases import users as users_usecases
from app.utils.token import Token
import json
import pprint

security = HTTPBearer()

async def logged_in(credentials: HTTPBasicCredentials = Depends(security), db: AsyncSession = Depends(get_db)):
    token = credentials.credentials
    token_data =  Token.validate_token(token)
    status_code, success, message, data = await users_usecases.auth(token_data.user_id, db)

    data_json = json.loads(data)

    if data_json["is_active"] == False:
        return status.HTTP_403_FORBIDDEN , False, f"You are not a active user!", None
    
    if success==False:
        return status.HTTP_401_UNAUTHORIZED , False, f"Unauthorized!", None

    return status_code, success, message, data