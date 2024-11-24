from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://mongodb:27017/ecommerce")
mongo = PyMongo(app)

@app.route('/api/profile/<user_id>', methods=['GET'])
def get_profile(user_id):
    profile = mongo.db.users.find_one({'user_id': user_id})
    if profile:
        profile['_id'] = str(profile['_id'])
        return jsonify(profile)
    return jsonify({'error': 'Profile not found'}), 404

@app.route('/api/profile/<user_id>', methods=['PUT'])
def update_profile(user_id):
    data = request.get_json()
    data['updated_at'] = datetime.utcnow()
    result = mongo.db.users.update_one(
        {'user_id': user_id},
        {'$set': data},
        upsert=True
    )
    return jsonify({'success': True})

@app.route('/api/profile/<user_id>/orders', methods=['GET'])
def get_user_orders(user_id):
    orders = list(mongo.db.orders.find({'user_id': user_id}))
    for order in orders:
        order['_id'] = str(order['_id'])
    return jsonify(orders)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)