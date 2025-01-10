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
import pprint


async def auth(user_id:int, db:AsyncSession):
    user_repo = UserRepository(db)

    try:
        user_data: User = await user_repo.get_with_role(user_id)

        if not user_data:
            return status.HTTP_404_NOT_FOUND, False, "User not found!", None

        new_data_resp = UserResponse(
            id=user_data.id,
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            is_active=user_data.is_active,
            role=RoleResponse.model_validate(user_data.role.__dict__.copy()) if user_data.role else None
        )

        new_data_json = new_data_resp.model_dump_json()

        return status.HTTP_200_OK, True, "Authenticated!", new_data_json

    except Exception as e:
        return status.HTTP_500_INTERNAL_SERVER_ERROR, False, f"Something went wrong with user data: {e}", None
        


async def login(user_credentials:LoginRequest, db: AsyncSession):
    user_repo = UserRepository(db)

    try:
        user_exists = await user_repo.get_by_userneme_or_email(user_credentials.identifier)
        if not user_exists:
            return status.HTTP_404_NOT_FOUND, False, f"User not found!", None

        if not user_exists.is_active:
            return status.HTTP_401_UNAUTHORIZED, False, f"You are not a active user!", None

        verify_password = PasswordHasher.verify_password(user_credentials.password, user_exists.hashed_password)
        if not verify_password:
            return status.HTTP_401_UNAUTHORIZED, False, f"Wrong password!", None
        
        access_token = Token.create_access_token({"sub": user_exists.id})        
        return status.HTTP_200_OK, False, f"Access granted!", {"access_token": access_token, "token_type": "bearer"}
    
    except Exception as e:
        return status.HTTP_500_INTERNAL_SERVER_ERROR, False, f"Something went wrong with user data: {e}", None
    

async def signup(user_data: UserRequest, db: AsyncSession):
    user_repo = UserRepository(db)
    role_repo = RoleRepository(db)

    try:
        # if email exist
        user_exists = await user_repo.get_by_field("email", user_data.email)
        if user_exists:
            return status.HTTP_409_CONFLICT, False, "Email is already registered!", None

        # if username exist
        user_exists = await user_repo.get_by_field("username", user_data.username)
        if user_exists:
            return status.HTTP_409_CONFLICT, False, "Username already exists!", None


        role = await role_repo.get_by_field("role", user_data.role.value)
        if not role:
            return status.HTTP_404_NOT_FOUND, False, "Role not found!", None

        admin_role = await role_repo.get_by_field("role", RoleEnum.ADMIN.value)
        
        # if admin exist
        admin_exist = await user_repo.get_by_field("role_id", admin_role.id)
        if admin_exist and role.id == admin_role.id:
            return status.HTTP_409_CONFLICT, False, "Admin already exists!", None


        hashed_password = PasswordHasher.hash_password(user_data.password)

        user_db_in = UserWithRoleId(**user_data.model_dump(), hashed_password=hashed_password, role_id=role.id)

    
        new_user:User = await user_repo.create(data=user_db_in.model_dump())

        new_data_resp = UserResponse(
                id=new_user.id,
                username=new_user.username,
                email=new_user.email,
                full_name=new_user.full_name,
                is_active=new_user.is_active,
                role=RoleResponse.model_validate(new_user.role.__dict__.copy()) if new_user.role else None
            )

        new_data_json = new_data_resp.model_dump_json()

        return status.HTTP_201_CREATED, True, "Signup successfull!", new_data_json
    except Exception as e:
        return status.HTTP_500_INTERNAL_SERVER_ERROR, False, f"Something went wrong with user data: {e}", None
    