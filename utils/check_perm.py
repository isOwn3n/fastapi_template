from http import HTTPStatus
from fastapi import HTTPException
from enum import Enum


class ResourceValue(Enum):
    """Enum for resource permission value"""

    ADD = 1
    VIEW = 2
    EDIT = 3
    DELETE = 4


def get_resource_value(resource):
    """Get resource value"""
    stat = {1: "add", 2: "view", 3: "edit", 4: "delete"}
    for key, val in stat.items():
        if val == resource:
            return key
    return None


async def has_access(
    roles: list[str], resource: str, status, repo
) -> bool:
    access = resources(roles, repo)
    stat = status
    if stat == None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        )
    if "superuser" in roles:
        return True
    else:
        for i, _ in enumerate(access):
            if access[i][0] == resource and access[i][stat]:
                return True
        return False

async def resources(roles, repo) -> list:
    """Get resources"""
    role_resource = []
    for role in roles:
        role_resource.append(await repo.get_role_resource(role))
    
    return role_resource