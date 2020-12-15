from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_cors import CORS

# Init app
app = Flask(__name__)
# To avoid CORS security problems
CORS(app)
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


# Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty


# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')


# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@app.route('/')
def home():
    return "Work"


# Create produce
@app.route('/products', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, price, qty)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


@app.route('/products', methods=['GET'])
def get_product():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


@app.route('/product/<item>', methods=['GET'])
def get_product_item(item):
    all_products = Product.query.filter_by(id=item)
    result = products_schema.dump(all_products)
    return jsonify(result)


@app.route('/product/<item>', methods=['PATCH'])
def update_product(item):
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    update = Product.query.filter_by(id=item).first()
    update.name = name
    update.description = description
    update.price = price
    update.qty = qty

    return product_schema.jsonify(update)


@app.route('/product/<item>', methods=['DELETE'])
def delete_product(item):
    delete = Product.query.filter_by(id=item).first()
    db.session.delete(delete)
    db.session.commit()

    return product_schema.jsonify(delete)


if __name__ == '__main__':
    app.run(debug=True)
