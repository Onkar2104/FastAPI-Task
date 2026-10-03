from pydantic import BaseModel, EmailStr


class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    course: str


class StudentUpdate(BaseModel):
    name: str
    email: EmailStr
    course: str


class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    course: str

    class Config:
        from_attributes = True



class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    isAdmin: bool

    class Config:
        from_attributes = True