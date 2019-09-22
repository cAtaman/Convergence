from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init Database
# global db
db = SQLAlchemy(app)

# Init marshmallow
ma = Marshmallow(app)


# Asset class
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)

    def __init__(self, name):
        self.name = name


# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


# init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@app.route('/')
def hello_world():
    return 'Hello World!'

# Create  product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']

    new_product = Product(name)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


# Get all products
@app.route('/products', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


# Run server
if __name__ == "__main__":
    app.run(debug=True)