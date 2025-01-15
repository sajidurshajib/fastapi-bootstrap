from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.profile_repo import ProfileRepository
from app.models import Profile
from app.schemas.profiles import ProfileResponse, ProfileUpdate
from app.utils.logger import Logger

logger = Logger(__name__)

async def get_profile(user_id:int, db:AsyncSession):
    
    profile_repo = ProfileRepository(db)

    try:
        profile_data: Profile = await profile_repo.get_by_field("user_id", user_id)

        if not profile_data:
            logger.info("Profile not found!")
            return status.HTTP_404_NOT_FOUND, False, "Profile not found!", None

        new_data_resp = ProfileResponse(
            address=profile_data.address,
            secondary_address=profile_data.secondary_address,
            phone=profile_data.phone,   
            secondary_phone=profile_data.secondary_phone,
            dob=profile_data.dob,
            sex=profile_data.sex
        )

        new_data_json = new_data_resp.model_dump_json()

        return status.HTTP_200_OK, True, "Profile found!", new_data_json

    except Exception as e:
        logger.error(f"Something went wrong with profile data: {e}")
        return status.HTTP_500_INTERNAL_SERVER_ERROR, False, f"Something went wrong with profile data: {e}", None




async def update(user_id:int, profile_data: ProfileUpdate, db: AsyncSession):

    profile_repo = ProfileRepository(db)

    try:
        profile_exists: Profile = await profile_repo.get_by_field("user_id", user_id)
        if not profile_exists:
            logger.info("Profile not found!")
            return status.HTTP_404_NOT_FOUND, False, "Profile not found!", None

        if profile_data.address:
            profile_exists.address = profile_data.address
        if profile_data.secondary_address:
            profile_exists.secondary_address = profile_data.secondary_address
        if profile_data.phone:
            profile_exists.phone = profile_data.phone
        if profile_data.secondary_phone:
            profile_exists.secondary_phone = profile_data.secondary_phone
        if profile_data.dob:
            profile_exists.dob = profile_data.dob
        if profile_data.sex:
            profile_exists.sex = profile_data.sex



        new_profile: Profile = await profile_repo.update(profile_exists.id, profile_exists.__dict__.copy())

        new_data_resp = ProfileResponse(
            address=new_profile.address,    
            secondary_address=new_profile.secondary_address,    
            phone=new_profile.phone,    
            secondary_phone=new_profile.secondary_phone,    
            dob=new_profile.dob,    
            sex=new_profile.sex
            )

        new_data_json = new_data_resp.model_dump_json()

        return status.HTTP_202_ACCEPTED, True, "Profile updated!", new_data_json
    except Exception as e:
        logger.error(f"Something went wrong with profile data: {e}")
        return status.HTTP_500_INTERNAL_SERVER_ERROR, False, f"Something went wrong with profile data: {e}", None