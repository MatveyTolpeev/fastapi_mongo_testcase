import enum
from pydantic import BaseModel
from typing import Union, List, Optional


class Sex(enum.Enum):
    man = 'М'
    women = 'Ж'
    unisex = 'У'


class Category(BaseModel):
    name: str
    slug: str


class Brand(BaseModel):
    name: str
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
    brand: Brand
    sex: Optional[str]
    material: Optional[str]
    root_category: Category
    price: Optional[float]
    discount_price: Optional[float]
    in_the_sale: bool
    leftovers: Optional[List[Leftover]]
