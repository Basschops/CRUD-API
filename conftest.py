import pytest

from config import conn_app, db
from models.item import Item


@pytest.fixture(scope="session")
def client():
    conn_app.add_api("spec.yaml")

    with conn_app.app.test_client() as c:
        yield c


@pytest.fixture(autouse=True)
def test_data():
    setup_data()
    yield
    Item.query.delete()


def setup_data():
    items_data = [
        {"file_name": "file1.mp4", "media_type": "mp4"},
        {"file_name": "file2.mp5", "media_type": "mp5"},
    ]
    items = []
    for item in items_data:
        item = Item(**item)
        items.append(item)
    db.bulk_save_objects(items)
    db.commit()
