from pydantic import BaseModel

class Token(BaseModel):
    access_token: str

class JWTData(BaseModel):
    user_id: str
    roles: list[str]

class LoginInfo(BaseModel):
    username: str
    password: str
