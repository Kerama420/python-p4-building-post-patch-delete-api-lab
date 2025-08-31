#!/usr/bin/env python3

from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


# GET all bakeries
@app.route('/bakeries', methods=['GET'])
def get_bakeries():
    bakeries = [b.to_dict() for b in Bakery.query.all()]
    return make_response(jsonify(bakeries), 200)


# GET bakery by id
@app.route('/bakeries/<int:id>', methods=['GET'])
def get_bakery(id):
    bakery = Bakery.query.get_or_404(id)
    return make_response(jsonify(bakery.to_dict()), 200)


# GET baked goods
@app.route('/baked_goods', methods=['GET'])
def get_baked_goods():
    goods = [g.to_dict() for g in BakedGood.query.all()]
    return make_response(jsonify(goods), 200)


# ✅ POST baked good
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    new_good = BakedGood(
        name=data.get('name'),
        price=data.get('price'),
        bakery_id=data.get('bakery_id')
    )
    db.session.add(new_good)
    db.session.commit()
    return make_response(jsonify(new_good.to_dict()), 201)


# ✅ PATCH bakery name
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get_or_404(id)
    data = request.form
    if "name" in data:
        bakery.name = data['name']
    db.session.commit()
    return make_response(jsonify(bakery.to_dict()), 200)


# ✅ DELETE baked good
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    good = BakedGood.query.get_or_404(id)
    db.session.delete(good)
    db.session.commit()
    return make_response(jsonify({"message": "Baked good deleted successfully"}), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
