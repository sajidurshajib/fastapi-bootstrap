from fastapi import status
from app.schemas.roles import RoleResponse
from app.repositories.role_repo import RoleRepository
from app.utils.responses import standard_response

async def roles(db):
    role_repo = RoleRepository(db)

    data = await role_repo.get_all(all=True)

    if data is None:
        return standard_response(status.HTTP_404_NOT_FOUND, False, "No data found!", data=[])
        

    data = [RoleResponse(role=dt.role, permissions=dt.permissions) for dt in data]
    results = [d.model_dump() for d in data]

    return standard_response(200, True, "Data available", data=results)
    