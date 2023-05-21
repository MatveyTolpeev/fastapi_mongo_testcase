# fastapi_mongo_testcase
This service use Fastapi to accept request from url with json and save it to mongodb with conditions.
# How to start with docker:
1) git clone https://github.com/MatveyTolpeev/fastapi_mongo_testcase.git
2) open terminal and change work direcotory to /fastapi_mongo_testcase
3) use docker-compose up --build -d

# How to start without docker:
firstly you need to intsall and start mongodb by yourself so i recommend to use docker, but use how you like it
1) git clone https://github.com/MatveyTolpeev/fastapi_mongo_testcase.git
2) change work direcotory to /fastapi_mongo_testcase
3) run main.py 

# How to use:
1) http://localhost:8000/ping - worktest, excepted answer {"success":true} methods=['GET]
2) http://localhost:8000/api/v1/data - get all data from data.json in browser methods=['GET]
3) http://localhost:8000/save_to_db - save all data from data.json in mongodb, take about 1-2 mins of time, methods=['GET]
4) http://localhost:8000/filtered_data - get data with filters, example of filter -> {"title":"юбка"}, methods=['POST'], not work in browser cause POST request type, try postman

# To make tests start file test.py
