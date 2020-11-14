# import flask libs
from flask_restful import Resource, reqparse
from flask import request
from datetime import datetime
from constants import constants
#from flask_jwt import jwt_required

from models.orders import OrderModel

class Order(Resource):
    # to handle HTTP GET /orders/<int:id>
    def get(self, id):
        order = OrderModel.find_by_id(id)
        if order:
            return order.json(), 200
        else:
            return {'Message': constants['ID_NOT_FOUND']}

    # to handle HTTP DEL /orders/<int:id>
    def delete(self, id):
        # checks if material exists in database
        order = OrderModel.find_by_id(id)

        # in case it exists, delete it
        if order:
            order.delete_from_db()
            
        # return message and default HTTP status (200 - OK)
        return {'Message': constants['DELETED']}

class Orders(Resource):
    # parser to handle POST request for /order route
    parser = reqparse.RequestParser();
    parser.add_argument('product_id',type=int,required=True);
    parser.add_argument('customer_id',type=int,required=True);
    parser.add_argument('notes',type=str,required=False);

    # handles HTTP request GET /orders
    def get(self):
        return [x.json() for x in OrderModel.query.all()]

    # handles HTTP request POST /orders
    def post(self):
        # gets parameter from parser
        data = Orders.parser.parse_args()
        
        # creates a new order
        order = OrderModel(**data)

        # tries to insert in database, returns 500 (internal server error) in case of database failure
        try:
            order.save_to_db()
        except:
            return {"Error Message": "An error occurred upon inserting the item into the database."}, 500

        # returns JSON with the created Material and returns CREATED status (201)
        return order.json(), 201
