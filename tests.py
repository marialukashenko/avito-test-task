import requests
import pytest

BASE_URL_1 = "https://qa-internship.avito.com/api/1"
BASE_URL_2 = "https://qa-internship.avito.com/api/2"

VALID_ITEM_ID = "56e36e04-2dd6-41c9-9b67-6307bdcc3197"
INVALID_ITEM_ID = "56e36e04-2dd6-41c9-9b67-6307bdcc3198"
INVALID_FORMAT_ID = "invalid-uuid"
VALID_SELLER_ID = 1
INVALID_SELLER_ID = "abc"

@pytest.fixture
def valid_item_id():
    """Фикстура для получения валидного ID объявления"""
    response = requests.get(f"{BASE_URL_1}/{VALID_SELLER_ID}/item")
    assert response.status_code == 200, f"Не удалось получить объявления, статус {response.status_code}"
    data = response.json()
    assert len(data) > 0, "Список объявлений пустой"
    return data[0]["id"]

def test_get_statistic_success():
    response = requests.get(f"{BASE_URL_2}/statistic/{VALID_ITEM_ID}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for item in data:
        assert "likes" in item and isinstance(item["likes"], int)
        assert "viewCount" in item and isinstance(item["viewCount"], int)
        assert "contacts" in item and isinstance(item["contacts"], int)

def test_get_statistic_not_found():
    response = requests.get(f"{BASE_URL_2}/statistic/{INVALID_ITEM_ID}")
    assert response.status_code == 404
    data = response.json()
    assert "result" in data and "status" in data

def test_delete_item_success(valid_item_id):
    response = requests.delete(f"{BASE_URL_2}/item/{valid_item_id}")
    assert response.status_code == 200
    assert response.text == ""

def test_delete_item_not_found():
    response = requests.delete(f"{BASE_URL_2}/item/{INVALID_ITEM_ID}")
    assert response.status_code == 404
    data = response.json()
    assert "result" in data and "status" in data

def test_delete_item_bad_request():
    response = requests.delete(f"{BASE_URL_2}/item/{INVALID_FORMAT_ID}")
    assert response.status_code == 400
    data = response.json()
    assert "result" in data and "status" in data

def test_get_item_not_found():
    response = requests.get(f"{BASE_URL_1}/item/{INVALID_ITEM_ID}")
    assert response.status_code == 404
    data = response.json()
    assert "result" in data and "status" in data

def test_get_item_bad_request():
    response = requests.get(f"{BASE_URL_1}/item/{INVALID_FORMAT_ID}")
    assert response.status_code == 400
    data = response.json()
    assert "result" in data and "status" in data

def test_post_item_bad_request():
    payload = {}  # пустой объект
    response = requests.post(f"{BASE_URL_1}/item", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "result" in data and "status" in data

def test_get_all_items_success():
    response = requests.get(f"{BASE_URL_1}/{VALID_SELLER_ID}/item")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for item in data:
        assert "id" in item
        assert "sellerId" in item

def test_get_all_items_bad_request():
    response = requests.get(f"{BASE_URL_1}/{INVALID_SELLER_ID}/item")
    assert response.status_code == 400
    data = response.json()
    assert "result" in data and "status" in data
