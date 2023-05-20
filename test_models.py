import enum


class Category:
    name: str
    slug: str


class Brand:
    name: str
    slug: str


class Sex(enum.Enum):
    man = 1
    women = 2
    unisex = 3


class Clothes:
    title: str
    SKU: str
    color: str
    brand: Brand
    sex: Sex
    material: str
    root_category: Category
    price: float
    
