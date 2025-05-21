from pydantic import BaseModel, EmailStr, ConfigDict

# User schema
class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    username: str
    password: str

    model_config = ConfigDict(extra='forbid')

class UserSchema(UserCreateSchema):
    id: int

class UserLoginSchema(BaseModel):
    username: str
    password: str

# Task schema
class TaskCreateSchema(BaseModel):
    title: str
    details: str
    user_id: int

    model_config = ConfigDict(extra='forbid')

class TaskSchema(TaskCreateSchema):
    id: int