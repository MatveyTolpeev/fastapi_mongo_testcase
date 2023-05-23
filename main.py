import traceback
from typing import List

import motor.motor_asyncio
from fastapi.routing import APIRoute, APIRouter
import uvicorn as uvicorn
from fastapi import Request, FastAPI, UploadFile, File, Body
import requests
from pymongo import MongoClient
from starlette.responses import JSONResponse
from models import Category, Product, Brand, Leftover
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
    search_arr_ends = ['-1', '-2', '-3', '-5', '-6', '-7', '-8', '-9', '-r', '-p']
    products = [
        Product(
            title=products_dict["title"],
            sku="" if str(products_dict["sku"]).find("---") != -1
            else str(products_dict["sku"])[:-2]
            if any([x in products_dict["root_category"] for x in search_arr])
                and any(str(products_dict["sku"]).endswith(end) for end in search_arr_ends)
            else str(products_dict["sku"])[:-4] if str(products_dict["sku"]).endswith('-r-r')
                and any([x in products_dict["root_category"] for x in search_arr])
            else str(products_dict["sku"]),
            color=str(products_dict["color"]).split("/")[1] if len(str(products_dict["color"]).split("/")) > 1 and
                                                               "Косметика" not in str(
                products_dict["root_category"]) else "",
            color_code=str(products_dict["color"]).split("/")[0] if len(str(products_dict["color"]).split("/")) > 0 and
                                                                    "Косметика" not in str(
                products_dict["root_category"]) else "",
            brand=products_dict["brand"],
            sex=products_dict["sex"],
            material=products_dict["material"],
            root_category=products_dict["root_category"],
            price=products_dict["discount_price"] if products_dict["discount_price"] > 0 and
            products_dict['discount_price'] < products_dict['price']
            else products_dict["price"],
            discount_price=0 if products_dict["discount_price"] >= products_dict["price"]
            else products_dict["discount_price"],
            in_the_sale=products_dict["in_the_sale"],
            leftovers=products_dict["leftovers"])
        for products_dict in products_list
    ]
    print(len(products))
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


def first_save_to_db():
    db = get_database()
    collection = db["products"]
    collection_categories = db['categories']
    collection_brands = db["brands"]
    count = 0
    try:
        for el in accept_data():
            if count % 1000 == 0:
                print(count)
            if collection.find_one({"sku": el.sku, "color": el.color, "color_code": el.color_code}) is None:
                if collection_categories.find_one({"title": el.root_category}) is None:
                    collection_categories.insert_one({"title": el.root_category, "slug": slugify(el.root_category)})
                if collection_brands.find_one({"title": el.brand}) is None:
                    collection_brands.insert_one({"title": el.brand, "slug": slugify(el.brand)})
                collection.insert_one(el.dict())
                count += 1
                continue
            cur = collection.find_one({"sku": el.sku, "color": el.color, "color_code": el.color_code})
            for el_leftover in el.leftovers:
                if any(temp_cur_leftover["size"] == el_leftover.size for temp_cur_leftover in cur["leftovers"]):
                    for cur_leftover in cur["leftovers"]:
                        if cur_leftover["size"] == el_leftover.size:
                            cur_leftover["count"] += el_leftover.count
                else:
                    cur["leftovers"] = cur["leftovers"] + [el_leftover.dict()]
            collection.replace_one({"sku": el.sku, "color": el.color, "color_code": el.color_code}, cur)
            count += 1
    except Exception as e:
        try:
            drop_collection("products")
        except Exception as e2:
            print(f"Unsuccess operation, no connection to db: {e}, {traceback.format_exc()}")
            return {"status": "connect_db_error"}
        print(f"Unsuccess operation, problem with save data: {e}, {traceback.format_exc()}")
        return {"status": "save_to_db_error"}


def update_to_db():
    db = get_database()
    collection = db["products"]
    collection_categories = db["categories"]
    collection_brands = db["brands"]
    count = 0
    try:
        for el in accept_data():
            if count % 1000 == 0:
                print(count)
            if collection.find_one({"sku": el.sku, "color": el.color, "color_code": el.color_code}) is None:
                if collection_categories.find_one({"title": el.root_category}) is None:
                    collection_categories.insert_one({"title": el.root_category, "slug": slugify(el.root_category)})
                if collection_brands.find_one({"title": el.brand}) is None:
                    collection_brands.insert_one({"title": el.brand, "slug": slugify(el.brand)})
                collection.insert_one(el.dict())
                count += 1
                continue
            cur = collection.find_one({"sku": el.sku, "color": el.color, "color_code": el.color_code})
            cur["leftovers"] = [lf.dict() for lf in el.leftovers]
            collection.replace_one({"sku": el.sku, "color": el.color, "color_code": el.color_code}, cur)
            count += 1
    except Exception as e:
        try:
            drop_collection("products")
        except Exception as e2:
            print(f"Unsuccess operation, no connection to db: {e}, {traceback.format_exc()}")
            return {"status": "connect_db_error"}
        print(f"Unsuccess operation, problem with save data: {e}, {traceback.format_exc()}")
        return {"status": "save_to_db_error"}


def get_filtered_data(filter: dict = Body(...)) -> List[dict]:
    db = get_database()

    # Not workling
    # products = db.products.find({"leftovers.count": { "$gt": 0}})

    #And it not working too
    # products = db.products.find({
    #     "leftovers": {
    #         "$elemMatch": {
    #             "count": {"$gt": 0}
    #         }
    #     }
    # })

    collection = db["products"]

    products = []
    for product in collection.find(filter, {"_id": 0},):
        for leftover in product["leftovers"]:
            if leftover["count"] > 0:
                products.append(product)
                break
    return products


routes = [
    APIRoute(path="/ping", endpoint=test_work, methods=['GET']),
    APIRoute(path="/api/v1/data", endpoint=send_data, methods=['GET']),
    APIRoute(path="/save_to_db", endpoint=first_save_to_db, methods=['GET']),
    APIRoute(path="/update_to_db", endpoint=update_to_db, methods=['GET']),
    APIRoute(path="/filtered_data", endpoint=get_filtered_data, methods=['POST'])
]

app.include_router(APIRouter(routes=routes))

if __name__ == "__main__":

    print(MONGODB_URL)
    print(get_database().name)
    uvicorn.run(app, host="localhost", port=8000)
