from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://mongodb:27017/ecommerce")
mongo = PyMongo(app)

@app.route('/api/stock/<product_id>', methods=['GET'])
def get_stock(product_id):
    stock = mongo.db.stock.find_one({'product_id': product_id})
    if stock:
        stock['_id'] = str(stock['_id'])
        return jsonify(stock)
    return jsonify({'quantity': 0})

@app.route('/api/stock/<product_id>', methods=['PUT'])
def update_stock(product_id):
    data = request.get_json()
    result = mongo.db.stock.update_one(
        {'product_id': product_id},
        {'$set': {'quantity': data['quantity']}},
        upsert=True
    )
    return jsonify({'success': True})

@app.route('/api/stock/batch', methods=['POST'])
def check_stock_batch():
    data = request.get_json()
    product_ids = data.get('product_ids', [])
    stock_levels = {}
    for product_id in product_ids:
        stock = mongo.db.stock.find_one({'product_id': product_id})
        stock_levels[product_id] = stock['quantity'] if stock else 0
    return jsonify(stock_levels)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)