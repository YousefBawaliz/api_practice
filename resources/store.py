import uuid
from flask import request
from flask_smorest import Blueprint,abort
from flask.views import MethodView 
from db import db
from models import StoreModel
from schemas import StoreSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError



## a blueprint is a way to organize your Flask application into modules

blp = Blueprint("store", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):

    @blp.response(200, StoreSchema)
    def get(self, store_id):
        """
        Get a store by ID.
        """
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        """
        Delete a store by ID.
        """
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted."}


@blp.route("/store")
class StoreList(MethodView):

    @blp.response(200,StoreSchema(many=True))
    def get(self):
        """
        Get all stores.
        """
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201,StoreSchema)
    def post(self, store_data):
        """
        Create a new store.
        """
        try:
            store = StoreModel(**store_data)
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return store