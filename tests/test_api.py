from freezegun import freeze_time
from unittest.mock import ANY

from models.item import Item


@freeze_time("2020-05-21T12:12:12")
def test_post_item(client):
    data = {"file_name": "my_media_file", "media_type": "png"}
    res = client.post("/items", json=data, content_type="application/json")
    assert res.status_code == 201
    assert res.json == {
        "id": ANY,
        "file_name": "my_media_file",
        "media_type": "png",
        "created_at": "2020-05-21T12:12:12",
        "updated_at": None,
    }


def test_post_item_missing_data(client):
    data = {"media_type": "png"}
    res = client.post("/items", json=data, content_type="application/json")
    assert res.status_code == 400
    assert res.json == {"file_name": ["Missing data for required field."]}

    data = {"file_name": "my_media_file"}
    res = client.post("/items", json=data, content_type="application/json")
    assert res.status_code == 400
    assert res.json == {"media_type": ["Missing data for required field."]}


def test_post_item_read_only(client):
    data = {"id": 1, "file_name": "my_media_file", "media_type": "png"}
    res = client.post("/items", json=data, content_type="application/json")
    assert res.status_code == 400
    assert res.json["detail"] == "Property is read-only - 'id'"


@freeze_time("2020-05-21T12:12:12")
def test_update_item(client):
    data = {"file_name": "updated_file", "media_type": "updated_png"}
    res = client.patch("/items/1", json=data, content_type="application/json")
    assert res.status_code == 201
    assert res.json == {
        "id": 1,
        "file_name": "updated_file",
        "media_type": "updated_png",
        "created_at": ANY,
        "updated_at": "2020-05-21T12:12:12",
    }


def test_update_item_partial(client):
    data = {"media_type": "updated_png2"}
    res = client.patch("/items/1", json=data, content_type="application/json")
    assert res.status_code == 201
    assert res.json["media_type"] == "updated_png2"


def test_update_item_read_only(client):
    data = {"id": 1, "file_name": "update", "media_type": "update_png"}
    res = client.patch("/items/1", json=data, content_type="application/json")
    assert res.status_code == 400
    assert res.json["detail"] == "Property is read-only - 'id'"


def test_update_item_not_found(client):
    data = {"file_name": "update", "media_type": "update_png"}
    res = client.patch("/items/555", json=data, content_type="application/json")
    assert res.status_code == 404
    assert res.json == "Not found"


def test_update_item_wrong_type(client):
    data = {"file_name": 1}
    res = client.patch("/items/555", json=data, content_type="application/json")
    assert res.status_code == 400
    assert res.json["detail"] == "1 is not of type 'string' - 'file_name'"

    data = {"media_type": 77}
    res = client.patch("/items/555", json=data, content_type="application/json")
    assert res.status_code == 400
    assert res.json["detail"] == "77 is not of type 'string' - 'media_type'"


def test_get_item(client):
    res = client.get("/items/1")
    assert res.status_code == 200
    assert res.json == {
        "created_at": ANY,
        "file_name": "file1.mp4",
        "id": 1,
        "media_type": "mp4",
        "updated_at": None,
    }


def test_get_item_not_found(client):
    res = client.get("/items/555")
    assert res.status_code == 404
    assert res.json == "Not found"


def test_get_items(client):
    res = client.get("/items")
    assert res.status_code == 200
    assert res.json == {
        "results": [
            {
                "created_at": ANY,
                "file_name": "file1.mp4",
                "id": 1,
                "media_type": "mp4",
                "updated_at": None,
            },
            {
                "created_at": ANY,
                "file_name": "file2.mp5",
                "id": 2,
                "media_type": "mp5",
                "updated_at": None,
            },
        ],
        "total": 2,
    }


def test_delete_item(client):
    res = client.delete("/items/1")
    assert res.status_code == 204
    item = Item.query.filter(Item.id == 1).one_or_none()
    assert item is None


def test_delete_item_not_found(client):
    res = client.delete("/items/555")
    assert res.status_code == 404
    assert res.json == "Not found"
