import motor.motor_asyncio
from fastapi.routing import APIRoute, APIRouter
import uvicorn as uvicorn
from fastapi import Request, FastAPI, UploadFile, File
import requests
from pymongo import MongoClient
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from test_models import Sex, Category, Product, Brand, Leftover
from envparse import Env
import json
from slugify import slugify

env = Env()
MONGODB_URL = env.str("MONGODB_URL", default="mongodb://localhost:27017/")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client["products"]


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    MONGODB_URL = env.str("MONGODB_URL", default="mongodb://localhost:27017/db")
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(MONGODB_URL)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['db']


# async def load_json(file: UploadFile = File(...)):
#     contents = await file.read()
#     products_list = [Product(
#         title=products_dict["title"],
#         sku=products_dict["sku"],
#         color=str(products_dict["color"]).split("/")[1],
#         color_code=str(products_dict["color"]).split("/")[0],
#         brand=Brand(name=products_dict["brand"],
#                     slug=slugify(products_dict["brand"])),
#         sex=products_dict["sku"],
#         material=products_dict["sku"],
#         root_category=Category(
#             name=products_dict["root_category"],
#             slug=products_dict["root_category"]),
#         price=products_dict["sku"],
#         discount_price=products_dict["sku"],
#         in_the_sale=products_dict["sku"],
#         leftovers=products_dict["sku"])
#                      if products_dict["root_category"] != "Косметика"
#                      else
#                      Product(
#                          title=products_dict["title"],
#                          sku=products_dict["sku"],
#                          color="",
#                          brand=Brand(name=products_dict["brand"],
#                                      slug=slugify(products_dict["brand"])),
#                          sex=products_dict["sku"],
#                          material=products_dict["sku"],
#                          root_category=Category(
#                              name=products_dict["root_category"],
#                              slug=products_dict["root_category"]),
#                          price=products_dict["sku"],
#                          discount_price=products_dict["sku"],
#                          in_the_sale=products_dict["sku"],
#                          leftovers=products_dict["sku"])
#                      for products_dict in json.loads(contents)]
#     # json_compatible_item_data = jsonable_encoder(Brand(name='Bal', slug='777'))
#     print(request.json())
#     return await request.json()


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


# def test_load_to_db():
#     product = Product(
#         title="кепка",
#         sku=str("87O338-1129204").split("-")[0],
#         color=str("005/коричнево-синий").split("/")[1],
#         color_code=str("005/коричнево-синий").split("/")[0],
#         brand=Brand(name="Corneliani",
#                     slug=slugify("Corneliani")),
#         sex="Ж",
#         material=" 69% шерсть, 29% шелк, 2% кашемир",
#         root_category=Category(name="Одежда аксессуары",
#                                slug=slugify("Одежда аксессуары")),
#         price=22320,
#         discount_price=22320,
#         in_the_sale=False,
#         leftovers=[Leftover(size=lf["size"],
#                             count=lf["count"],
#                             price=lf["price"])
#                    for lf in test_leftovers]
#     )
#     product2 = Product(
#         title="кепка2",
#         sku=str("87O3382-1129204").split("-")[0],
#         color=str("005/коричнево-синий").split("/")[1],
#         color_code=str("005/коричнево-синий").split("/")[0],
#         brand=Brand(name="Corneliani",
#                     slug=slugify("Corneliani")),
#         sex="М",
#         material=" 69% шерсть, 29% шелк, 2% кашемир",
#         root_category=Category(name="Одежда аксессуары",
#                                slug=slugify("Одежда аксессуары")),
#         price=22320,
#         discount_price=22320,
#         in_the_sale=False,
#         leftovers=[Leftover(size=lf["size"],
#                             count=lf["count"],
#                             price=lf["price"])
#                    for lf in test_leftovers]
#     )
#     product3 = Product(
#         title="кепка2",
#         sku=str("87O338-11292404").split("-")[0],
#         color=str("005/коричнево-синий").split("/")[1],
#         color_code=str("005/коричнево-синий").split("/")[0],
#         brand=Brand(name="Corneliani",
#                     slug=slugify("Corneliani")),
#         sex="М",
#         material=" 69% шерсть, 29% шелк, 2% кашемир",
#         root_category=Category(name="Одежда аксессуары",
#                                slug=slugify("Одежда аксессуары")),
#         price=22320,
#         discount_price=22320,
#         in_the_sale=False,
#         leftovers=[Leftover(size=lf["size"],
#                             count=lf["count"],
#                             price=lf["price"])
#                    for lf in test_leftovers2]
#     )
#     # print(product)
#     return [product, product2, product3]


def test_get_from_db():
    pass


def test_accept_data():
    products_list = requests.get("http://localhost:8000/api/v1/data").json()
    print(len(products_list))
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
            price=products_dict["price"],
            discount_price=products_dict["discount_price"],
            in_the_sale=products_dict["in_the_sale"],
            leftovers=products_dict["leftovers"])
        for products_dict in products_list
    ]
    # print(result[0]["sku"])
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
    result = test_accept_data()
    print(type(result[0]))
    print(result[0])
    db = get_database()
    collection = db["products"]
    for el in test_accept_data():
        print(f"сейчас мы на товаре: {el.title}")
        if collection.find_one({"sku": el.sku}) is None:
            collection.insert_one(el.dict())
            continue
        cur = collection.find_one({"sku": el.sku})
        for el_leftover in el.leftovers:
            if any(temp_cur_leftover["size"] == el_leftover.size for temp_cur_leftover in cur["leftovers"]):
                for cur_leftover in cur["leftovers"]:
                    if cur_leftover["size"] == el_leftover.size:
                        pass
                        print(f"размер {el_leftover.size} уже есть у товара {cur['title']}")
                        cur_leftover["count"] += el_leftover.count
            else:
                print(f"размер {el_leftover.size} ещё нет у товара {cur['title']}")
                cur["leftovers"] = cur["leftovers"] + [el_leftover.dict()]
        collection.replace_one({"sku": cur["sku"]}, cur)


routes = [
    APIRoute(path="/ping", endpoint=test_work, methods=['GET']),
    # APIRoute(path="/load_json", endpoint=load_json, methods=['POST']),
    APIRoute(path="/test_load", endpoint=test_accept_data, methods=['POST']),
    APIRoute(path="/api/v1/data", endpoint=send_data, methods=['GET']),
    APIRoute(path="/get_data", endpoint=test_accept_data, methods=['GET']),
    APIRoute(path="/save_to_db", endpoint=save_to_db, methods=['GET'])
]

app = FastAPI()
app.include_router(APIRouter(routes=routes))

if __name__ == "__main__":
    # db = get_database()
    # collection = db["products"]

    # for el in test_load_to_db():
    #     print(f"сейчас мы на товаре: {el.title}")
    #     if collection.find_one({"sku": el.sku}) is None:
    #         collection.insert_one(el.dict())
    #         continue
    #     cur = collection.find_one({"sku": el.sku})
    #     for el_leftover in el.leftovers:
    #         if any(temp_cur_leftover["size"] == el_leftover.size for temp_cur_leftover in cur["leftovers"]):
    #             for cur_leftover in cur["leftovers"]:
    #                 if cur_leftover["size"] == el_leftover.size:
    #                     pass
    #                     print(f"размер {el_leftover.size} уже есть у товара {cur['title']}")
    #                     cur_leftover["count"] += el_leftover.count
    #         else:
    #             print(f"размер {el_leftover.size} ещё нет у товара {cur['title']}")
    #             cur["leftovers"] = cur["leftovers"] + [el_leftover.dict()]
    #     collection.replace_one({"sku": cur["sku"]}, cur)

    uvicorn.run(app, host="localhost", port=8000)
