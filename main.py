from typing import List

import motor.motor_asyncio
from fastapi.routing import APIRoute, APIRouter
import uvicorn as uvicorn
from fastapi import Request, FastAPI, UploadFile, File, Body
import requests
from pymongo import MongoClient
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models import Sex, Category, Product, Brand, Leftover
from envparse import Env
import json
from slugify import slugify

env = Env()
MONGODB_URL = env.str("MONGODB_URL", default="mongodb://localhost:27017/")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client["products"]
app = FastAPI()

def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    MONGODB_URL = env.str("MONGODB_URL", default="mongodb://localhost:27017/db")
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(MONGODB_URL)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['db']


def drop_collection(collection_name: str):
    db = get_database()
    collection = db[collection_name]
    collection.drop()


test_leftovers = [
    {
        "size": "58",
        "count": 2,
        "price": 22820
    },
    {
        "size": "59",
        "count": 1,
        "price": 22820
    },
    # {
    #     "size": "60",
    #     "count": 2,
    #     "price": 22820
    # },
]

test_leftovers2 = [
    {
        "size": "48",
        "count": 2,
        "price": 22820
    },
    {
        "size": "49",
        "count": 1,
        "price": 22820
    },
    # {
    #     "size": "60",
    #     "count": 2,
    #     "price": 22820
    # },
]


def accept_data():
    products_list = requests.get("http://localhost:8000/api/v1/data").json()
    search_arr = ["Обувь", "Одежда", "Сумки"]
    products = [
        Product(
            title=products_dict["title"],
            sku="" if str(products_dict["sku"]).find("--") != -1
            else str(products_dict["sku"]).split('-')[0]
            if any([x in products_dict["root_category"] for x in search_arr]) else str(products_dict["sku"]),
            color=str(products_dict["color"]).split("/")[1] if len(str(products_dict["color"]).split("/")) > 1 and
                        "Косметика" not in str(products_dict["root_category"]) else "",
            color_code=str(products_dict["color"]).split("/")[0] if len(str(products_dict["color"]).split("/")) > 0 and
                         "Косметика" not in str(products_dict["root_category"]) else "",
            brand=Brand(name=products_dict["brand"],
                        slug=slugify(products_dict["brand"])),
            sex=products_dict["sex"],
            material=products_dict["material"],
            root_category=Category(
                name=products_dict["root_category"],
                slug=slugify(products_dict["root_category"])),
            price=products_dict["discount_price"] if products_dict["discount_price"] > 0
            else products_dict["price"],
            discount_price=0 if products_dict["discount_price"] >= products_dict["price"]
            else products_dict["discount_price"],
            in_the_sale=products_dict["in_the_sale"],
            leftovers=products_dict["leftovers"])
        for products_dict in products_list
    ]
    return products


def send_data(request: Request):
    # Request не обязателен
    data = None
    with open("data.json", "r", encoding='utf-8') as f:
        data = json.load(f)
    if data:
        return JSONResponse(content=data)
    return JSONResponse({"status": "n"})


def test_work(request: Request):
    return JSONResponse(content={"success": True})


def save_to_db():
    drop_collection("products")
    db = get_database()
    collection = db["products"]
    count = 0
    for el in accept_data():
        if count % 1000 == 0:
            print(count)
        if collection.find_one({"sku": el.sku}) is None:
            collection.insert_one(el.dict())
            continue
        cur = collection.find_one({"sku": el.sku})
        for el_leftover in el.leftovers:
            if any(temp_cur_leftover["size"] == el_leftover.size for temp_cur_leftover in cur["leftovers"]):
                for cur_leftover in cur["leftovers"]:
                    if cur_leftover["size"] == el_leftover.size:
                        pass
                        cur_leftover["count"] += el_leftover.count
            else:
                cur["leftovers"] = cur["leftovers"] + [el_leftover.dict()]
        collection.replace_one({"sku": cur["sku"]}, cur)
        count += 1


def get_filtered_data(filter: dict = Body(...)) -> List[dict]:

    db = get_database()
    collection = db["products"]

    products = []
    for product in collection.find(filter, {"_id": 0}):
        products.append(product)
    print(len(products))
    return products


routes = [
    APIRoute(path="/ping", endpoint=test_work, methods=['GET']),
    APIRoute(path="/api/v1/data", endpoint=send_data, methods=['GET']),
    APIRoute(path="/save_to_db", endpoint=save_to_db, methods=['GET']),
    APIRoute(path="/filtered_data", endpoint=get_filtered_data, methods=['POST'])
]


app.include_router(APIRouter(routes=routes))

if __name__ == "__main__":
    print("testprint_in_docker")
    print(MONGODB_URL)
    print(get_database().name)
    uvicorn.run(app, host="localhost", port=8000)
