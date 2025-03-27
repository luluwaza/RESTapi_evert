from pydantic import BaseModel


class UserRead(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    hashed_password: (
        str  # You might eventually want to accept raw password and hash here
    )
    role: str
