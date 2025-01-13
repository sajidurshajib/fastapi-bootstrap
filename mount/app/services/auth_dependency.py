from fastapi import Depends, status
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.connection import get_db
from app.usecases import users as users_usecases
from app.utils.token import Token
from app.utils.logger import Logger
import json
import pprint

security = HTTPBearer()

logger = Logger(__name__)

async def logged_in(
    credentials: HTTPBasicCredentials = Depends(security), 
    db: AsyncSession = Depends(get_db)
    ):

    try:
        token = credentials.credentials
        token_data =  Token.validate_token(token)
        status_code, success, message, data = await users_usecases.auth(token_data.user_id, db)

        data_json = json.loads(data)

        if data_json["is_active"] == False:
            logger.info(f"You are not a active user!")
            return status.HTTP_403_FORBIDDEN , False, f"You are not a active user!", None
        
        if success==False:
            logger.info(f"Unauthorized!")
            return status.HTTP_401_UNAUTHORIZED , False, f"Unauthorized!", None

        return status_code, success, message, data

    except Exception as e:
        logger.error(f"Something went wrong with auth data: {e}")
        return status.HTTP_500_INTERNAL_SERVER_ERROR, False, f"Something went wrong with auth data: {e}", None


def has_permission(required_permission):
    async def permission_checker(
        credentials: HTTPBasicCredentials = Depends(security),
        db: AsyncSession = Depends(get_db)
        ):
        
        try:
            status_code, success, message, data = await logged_in(credentials, db)

            data_json = json.loads(data)
            user_permissions = data_json["role"]["permissions"]

            print("-"*10)
            pprint.pprint(user_permissions)
            print("-"*10)

            if required_permission not in user_permissions:
                logger.info(f"You don't have permission to access this resource!")
                return status.HTTP_403_FORBIDDEN , False, f"You don't have permission to access this resource!", None
            
            return status_code, success, message, data
        except Exception as e:
            logger.error(f"Something went wrong with auth data: {e}")
            return status.HTTP_500_INTERNAL_SERVER_ERROR, False, f"Something went wrong with auth data: {e}", None

    return permission_checker