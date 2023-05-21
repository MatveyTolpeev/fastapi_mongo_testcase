import requests
from pymongo import MongoClient
import json
from fastapi.testclient import TestClient
from main import app
from main import get_database

client = TestClient(app)


def test_get_database():
    expected_db_name = 'db'
    expected_client = MongoClient('mongodb://localhost:27017/db')

    actual_db = get_database()
    actual_db_name = actual_db.name
    actual_client = actual_db.client

    assert actual_db_name == expected_db_name
    assert actual_client == expected_client


def test_send_data():
    response = client.get("/api/v1/data")
    assert response.status_code == 200
    assert response.json() is not None


def test_work():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"success": True}


def test_get_filtered_data():
    filter = {"brand": "Nike"}
    response = client.post("/filtered_data", json={"filter": filter})
    assert response.status_code == 200
    assert response.json() is not None
