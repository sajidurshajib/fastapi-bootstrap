from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repo import UserRepository
from app.repositories.role_repo import RoleRepository
from app.models import User
from app.schemas.users import UserWithRoleId, UserResponse, UserRequest, LoginRequest
from app.schemas.roles import RoleResponse
from app.utils.password_utils import PasswordHasher
from app.utils.token import Token
from app.enums.roles import RoleEnum
from app.utils.logger import Logger
import json


logger = Logger(__name__)

async def search(key:str, role: str, is_active:bool, offset:int, limit:int, db:AsyncSession):
    user_repo = UserRepository(db)

    try:
        users = await user_repo.search(key, role, is_active, offset, limit)
        if users:
            all_users = []
            for user in users:
                user_resp = UserResponse(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    full_name=user.full_name,
                    is_active=user.is_active,
                    role=RoleResponse.model_validate(user.role.__dict__.copy()) if user.role else None
                )
                all_users.append(json.loads(user_resp.model_dump_json()))

            all_data = {
                "offset": offset,
                "limit": limit,
                "total": len(all_users),
                "users": all_users,
            }
            return status.HTTP_200_OK, True, "Users found!", all_data
        else:
            return status.HTTP_200_OK, True, "Users not found!", {}

    except Exception as e:
        logger.error(f"Something went wrong with user data: {e}")
        return status.HTTP_500_INTERNAL_SERVER_ERROR, False, f"Something went wrong with user data: {e}", None
    
async def user_status_change(user_id : int, db:AsyncSession):
    user_repo = UserRepository(db)

    try:
        user:User = await user_repo.get_by_field("id",user_id)
        if user:
            if user.is_active:
                user.is_active = False
            else:
                user.is_active = True
            await user_repo.update(user_id, user.__dict__.copy())
            await db.commit()
            return status.HTTP_200_OK, True, "User status changed!", {"is_active":user.is_active}
        else:
            return status.HTTP_404_NOT_FOUND, False, "User not found!", None

    except Exception as e:
        logger.error(f"Something went wrong with user data: {e}")
        return status.HTTP_500_INTERNAL_SERVER_ERROR, False, f"Something went wrong with user data: {e}", None
