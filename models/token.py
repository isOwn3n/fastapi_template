from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, DateTime, Column


class RevokeToken(SQLModel, table=True):
    __tablename__ = "revoke_token"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    token: str
    rev_date: datetime = Field(
        default=datetime.now(),
        sa_column=Column(DateTime(timezone=True)),
    )
    logged_out: bool = False
