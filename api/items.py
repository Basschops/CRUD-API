from connexion import NoContent

from models.item import Item
from schemas.item import ItemSchema
from config import db

db_session = db


def get(id):
    item = Item.query.filter(Item.id == id).one_or_none()
    if item is None:
        return "Not found", 404
    return ItemSchema().dump(item), 200


def post(body):
    data = ItemSchema().load(body)
    item = Item(**data)
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    return ItemSchema().dump(item), 201


def search():
    items = db_session.query(Item).all()
    response = ItemSchema().dump(items, many=True)
    return {"total": len(response), "results": response}, 200


def update(id, body):
    item = db_session.query(Item).filter(Item.id == id).one_or_none()
    if item is not None:
        data = ItemSchema().load(body, partial=True)
        item.update(**data)
        db_session.commit()
        return ItemSchema().dump(item), 201
    else:
        return "Not found", 404


def delete(id):
    item = Item.query.filter(Item.id == id).one_or_none()
    if item is not None:
        db_session.query(Item).filter(Item.id == id).delete()
        db_session.commit()
        return NoContent, 204
    else:
        return "Not found", 404
