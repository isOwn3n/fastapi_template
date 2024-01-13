from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from .user import User


class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    roleName: str
    roleDesc: str | None = Field(default=None)

    # User Role FK
    user_role: List["User_Role"] = Relationship(back_populates="role")

    # Resource Role FK
    resource_role: List["Resource_Role"] = Relationship(back_populates="role")

    created_at: datetime | None = Field(default=None, nullable=True)
    updated_at: datetime | None = Field(default=None, nullable=True)


class User_Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="user_role")

    role_id: Optional[int] = Field(default=None, foreign_key="role.id")
    role: Optional[Role] = Relationship(back_populates="user_role")

    created_at: datetime | None = Field(default=None, nullable=True)
    updated_at: datetime | None = Field(default=None, nullable=True)


class Resource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    resourceName: str
    resourceDesc: str

    # Resource Role FK
    resource_role: List["Resource_Role"] = Relationship(back_populates="resource")


    created_at: datetime | None = Field(default=None, nullable=True)
    updated_at: datetime | None = Field(default=None, nullable=True)


class Resource_Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    resource_id: Optional[int] = Field(default=None, foreign_key="resource.id")
    resource: Optional[Resource] = Relationship(back_populates="resource_role")

    role_id: Optional[int] = Field(default=None, foreign_key="role.id")
    role: Optional[Role] = Relationship(back_populates="resource_role")

    can_add: bool = Field(default=False)
    can_view: bool = Field(default=False)
    can_edit: bool = Field(default=False)
    can_delete: bool = Field(default=False)

    created_at: datetime | None = Field(default=None, nullable=True)
    updated_at: datetime | None = Field(default=None, nullable=True)
