from fastapi import status
from app.repositories.user_repo import UserRepository
import pprint

async def user_all(db, username, full_name, email, limit, offset):
    user_repo = UserRepository(db)

    users = await user_repo.get_all_by_multi_fields(limit=limit, offset=offset, username=username, full_name=full_name, email=email)
    
    if users is None:
        users = []
    
    return users

async def user_signup(user_data, db):
    user_repo = UserRepository(db)

    user_exist = await user_repo.get_by_field("email", user_data.get("email"))

    if user_exist:
        return status.HTTP_409_CONFLICT, False, "Email is already registered!", None

    try:
        new_user = await user_repo.create(data=user_data, commit=False)
    except Exception as e:
        return status.HTTP_500_INTERNAL_SERVER_ERROR, False, f"Something went wrong with user data: {e}", None
    
    await db.commit()