from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    name: str
    age: int
    conf_password: str
    ph_no: int
class LoginInput(BaseModel):
    email: str
    password: str