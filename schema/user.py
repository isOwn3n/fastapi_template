from pydantic import BaseModel

class UserGetResponse(BaseModel):
    username: str
    email: str

class UserCreateRequest(BaseModel):
    username: str
    email: str
    password: str

class UserUpdateRequest(BaseModel):
    username: str
    email: str

class UserChangePasswordRequest(BaseModel):
    password: str
    new_password: str