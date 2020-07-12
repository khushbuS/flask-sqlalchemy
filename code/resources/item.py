from flask import request
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = 'This field cannot be blank'
    )
    parser.add_argument('store_id',
            type = int,
            required = True,
            help = 'This field cannot be blank'
    )
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'Item with name {} already exists'.format(name)}, 400
        else:
            request_data = Item.parser.parse_args()
            item = ItemModel(name, request_data['price'], request_data['store_id'])
            try:
                item.save_to_db()
            except:
                {'message': 'An error occurred inserting the item'}, 500
            return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_item()
        return {'message': 'Item deleted'}

    def put(self, name):
        request_data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
             item = ItemModel(name, request_data['price'], request_data['store_id'])
        else:
            item.price = request_data['price']
            item.store_id = request_data['store_id']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda item: item.json(), ItemModel.query.all()))}
