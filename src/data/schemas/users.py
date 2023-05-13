from ._base import BaseModel


class UserBase(BaseModel):
    tg_id: int


class UserCreate(UserBase):
    ...


class UserView(UserBase):
    id: int

    class Config:
        orm_mode = True
