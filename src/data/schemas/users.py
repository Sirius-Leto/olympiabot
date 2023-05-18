from .__base import BaseModel
from .__mixins import IdMixin


class UserBase(BaseModel):
    tg_id: int


class UserCreate(UserBase):
    ...


class UserView(IdMixin, UserBase):
    class Config:
        orm_mode = True
