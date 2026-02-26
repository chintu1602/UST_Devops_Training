from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class Userlogin(UserCreate):
    class config:
        from_attributes=True


