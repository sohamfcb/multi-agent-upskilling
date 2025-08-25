# schemas/user.py
from datetime import datetime
from uuid import UUID
from typing import Optional, Annotated
from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator

# what you accept from the client (create OR update)
class UserIn(BaseModel):
    first_name: str = Field(..., max_length=20)
    last_name:  str = Field(..., max_length=30)
    email: EmailStr
    username: str = Field(..., max_length=50)
    password: str = Field(..., min_length=8, max_length=255)

# what you return to the client (never include password)
class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # allows returning ORM objects
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

class Login(BaseModel):
    # username: Annotated[str, Field(description="username of the user", examples=["someone231__"])]
    username: Optional[str] = Field(default=None, description="Username of the user", examples=["someone231__"])
    email: Optional[EmailStr] = Field(None, description="Email of the user")
    password: str = Field(..., description="Password")

    @model_validator(mode="after")
    def check_username_or_email(self):
        if not (self.username or self.email):
            raise ValueError("Either username or email must be provided.")
        return self

class TokenResponseSchema(BaseModel):
    access_token: Annotated[str, Field(..., description="")]
    refresh_token: str 
    token_type: Annotated[str, Field(default="bearer")]


class UpdateUsername(BaseModel):
    new_username: Annotated[str, Field(..., max_length=50)]

class UpdatePassword(BaseModel):
    new_password: Annotated[str, Field(...,min_length=10, max_length=255)]

class RefreshTokenSchema(BaseModel):
    refresh_token: str

class VerifySignUp(BaseModel):
    email: EmailStr
    code: str = Field(min_length=6, max_length=6, description="6 digit OTP code")