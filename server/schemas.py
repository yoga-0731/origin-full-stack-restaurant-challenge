from datetime import datetime
from typing import List, Optional, Any

from pydantic.utils import GetterDict
from pydantic import BaseModel


class UserRegistration(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        arbitrary_types_allowed = True


class LoginRequest(BaseModel):
    email: str
    password: str


class PlateBase(BaseModel):
    plate_name: str
    price: float
    picture: Optional[str] = None


class Plate(PlateBase):
    plate_id: int

    class Config:
        orm_mode = True


class PlateCount(Plate):
    order_count: int

    class Config:
        orm_mode = True


class PlateOrderBase(BaseModel):
    plate_id: int
    quantity: int
    user_id: int


class PlateOrderGetter(GetterDict):
    def get(self, key: str, default: Any = None) -> Any:
        if key in {'plate_name'}:
            return getattr(self._obj.plate, key)
        else:
            return super(PlateOrderGetter, self).get(key, default)


class PlateOrder(PlateOrderBase):
    plate_name: str
    class Config:
        orm_mode = True
        getter_dict = PlateOrderGetter


class OrderBase(BaseModel):
    plates: List[PlateOrderBase]
    

class Order(OrderBase):   
    order_id: int
    order_time: datetime
    plates: List[PlateOrder]
    status: str

    class Config:
        orm_mode = True


class ShoppingCart(BaseModel):
    id: Optional[int]
    user_id: int
    plate_id: int
    plate_quantity: int


class Review(BaseModel):
    id: Optional[int]
    user_id: int
    plate_id: int
    rating: int
    comment: str
