import enum
from pydantic import BaseModel
from typing import Union, List, Optional


class Sex(enum.Enum):
    man = 'М'
    women = 'Ж'
    unisex = 'У'


class Category(BaseModel):
    title: str
    slug: str


class Brand(BaseModel):
    title: str
    slug: str


class Leftover(BaseModel):
    size: Optional[str]
    count: Optional[int]
    price: Optional[int]


class Product(BaseModel):
    title: str
    sku: str
    color: str
    color_code: str
    brand: str
    sex: Optional[str]
    material: Optional[str]
    root_category: str
    price: Optional[float]
    discount_price: Optional[float]
    in_the_sale: bool
    leftovers: Optional[List[Leftover]]
