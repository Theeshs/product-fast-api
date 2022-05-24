import json
from urllib import response
import pytest
from fastapi.testclient import TestClient
from core.models.products import (
    Currencies
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, drop_database
from  main import create_app

from db._db import get_db, Base


@pytest.fixture
def db():
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:mysecretpassword@127.0.0.1:5432/testing_app"
    create_database(SQLALCHEMY_DATABASE_URL)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=True,
        future=True
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        db = TestingSessionLocal()
        cur1 = {
            "currency_name": "dollar",
            "currency_sign": "$"
        }
        cur2 = {
            "currency_name": "euro",
            "currency_sign": "€"
        }
        currency1 = Currencies(**cur1)
        currency2 = Currencies(**cur2)
        db.add(currency1)
        db.add(currency2)
        db.commit()
        yield db
    finally:
        drop_database(SQLALCHEMY_DATABASE_URL)
        db.close()



@pytest.fixture
def test_app(db):
    app = create_app()
    client = TestClient(app)
    yield client


def test_ping(test_app):
    response = test_app.get("/api/ping")
    res = response.json()
    assert res.get("data") == "pong"


def test_create(test_app):
    data = {
        "name": "test",
        "price": 10.00,
        "currency": 1
    }
    res = test_app.post("/api/products", json=data)
    response = res.json()
    assert response.get("name") == data.get("name")
    assert response.get("price") == data.get("price")
    assert response.get("currency_sign") == "$"
    assert response.get("currency_name") == "dollar"


def test_list_all_with_no_currency(test_app):
    res = test_app.get("/api/products")
    response = res.json()
    assert len(response) > 0
    assert response[0].get("name") is not None


def test_list_all_with_no_currency(test_app):
    res = test_app.get("/api/products?currency=1")
    response = res.json()
    assert len(response) > 0
    assert response[0].get("name") is not None
    for item in response:
        assert item.get("currency_sign") == "$"


def test_get_product_with_no_currency(test_app):
    data = [{
        "name": "test",
        "price": 10.00,
        "currency": 1
    },
    {
        "name": "test2",
        "price": 10.00,
        "currency": 2
    }]
    res = test_app.post("/api/products", json=data[0])
    create_response_1 = res.json()

    res = test_app.post("/api/products", json=data[1])
    create_response_2 = res.json()

    res = test_app.get(f"/api/products/{create_response_1.get('id')}")
    response = res.json()
    assert res.status_code == 200
    assert response.get("id") == create_response_1.get('id')
    assert response.get("id") != create_response_2.get('id')


def test_get_product_with_currency_and_id(test_app):
    data = [{
        "name": "test",
        "price": 10.00,
        "currency": 1
    },
    {
        "name": "test2",
        "price": 10.00,
        "currency": 2
    }]
    res = test_app.post("/api/products", json=data[0])
    create_response_1 = res.json()

    res = test_app.post("/api/products", json=data[1])

    res = test_app.get(f"/api/products/{create_response_1.get('id')}?currency=1")
    response = res.json()
    assert res.status_code == 200
    assert response.get("id") == create_response_1.get('id')
    assert response.get("currency_sign") == create_response_1.get('currency_sign')


def test_create_update_product(test_app):
    data = {
        "name": "test",
        "price": 10.00,
        "currency": 1
    }
    res = test_app.post("/api/products", json=data)
    create_response = res.json()

    data2 = {
        "name": "test_123",
        "price": 100.00,
        "currency": 1
    }

    res = test_app.put(f"/api/products/{create_response.get('id')}", json=data2)
    response = res.json()
    assert response.get("id") == create_response.get("id")
    assert response.get("name") == data2.get("name")
    assert response.get("price") == data2.get("price")
    assert response.get("name") != data.get("name")
    assert response.get("price") != data.get("price")


def test_delete_product_with_no_currency(test_app):
    data = {
        "name": "test",
        "price": 10.00,
        "currency": 1
    }
    res = test_app.post("/api/products", json=data)
    create_response = res.json()

    res = test_app.delete(f"/api/products/{create_response.get('id')}")
    response = res.json()
    assert response.get("id") == create_response.get("id")
    assert response.get("name") == create_response.get("name")
    assert response.get("price") == create_response.get("price")
    res = test_app.get(f"/api/products/{create_response.get('id')}")
    response = res.json()
    assert response.get("id") is None


def test_delete_product_with_currency(test_app):
    data = {
        "name": "test",
        "price": 10.00,
        "currency": 1
    }
    res = test_app.post("/api/products", json=data)
    create_response = res.json()

    res = test_app.delete(f"/api/products/{create_response.get('id')}?currency=1")
    response = res.json()
    assert response.get("id") == create_response.get("id")
    assert response.get("name") == create_response.get("name")
    assert response.get("price") == create_response.get("price")
    res = test_app.get(f"/api/products/{create_response.get('id')}?currency=1")
    response = res.json()
    assert response.get("id") is None