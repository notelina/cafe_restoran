from pydantic import BaseModel


class GuestCreate(BaseModel):
    name: str
    number: str


class GuestOut(BaseModel):
    id: int
    name: str
    number: str

    class Config:
        from_attributes = True


class DishCreate(BaseModel):
    name: str
    price: float


class DishOut(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True