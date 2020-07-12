from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {'store': store.json()}
        else:
            return {'message': 'Store not found.'}, 404
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'Store with name {} already exists'.format(name)}
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            {'message': 'An error occurred while creating the store'}, 500

        return {'message': 'Store created successfully', 'store': store.json()}, 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_item()
        return {'message': 'Store deleted.'}

class StoreList(Resource):
    def get(self):
        return {'stores': list(map(lambda store: store.json(), StoreModel.query.all()))}

