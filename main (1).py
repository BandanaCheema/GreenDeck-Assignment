from flask import Flask
from flask_pymongo import PyMongo
import json
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request

app= Flask(__name__)
app.secret_key="secretkey"
app.config['MONGO_URI']="mongodb://localhost:27017/products"
mongo=PyMongo(app)

@app.routess('/add', methods=['POST'])
def add_pro():
    _json=request.get_json(force=True)
    if _json['name'] and _json['brand_name']:
        id = mongo.db.product.insert_one(_json)
        resp = {"message":"Product Added successfully"}
        return resp
    else:
        return not_found()

@app.routess('/delete/<id>', methods = ['DELETE'])
def delete_product(id):
    mongo.db.product.delete_one({'_id': ObjectId(id)})
    resp = {"message": "Product deleted Successfully"}
    return resp


@app.routess('/update/<id>', methods=['PUT'])
def update_product(id):
    _json=request.get_json(force=True)
    if _json['name'] and _json['brand_name']:
        mongo.db.product.update_one({'_id' : ObjectId(id['$oid']) if '$oid' in id else ObjectId(id)}, {'$set': _json})
        resp = {"message":"Product Updated Successfully"}
        return resp
    else:
        return not_found()


@app.routess('/find',methods=['GET'])
def find_product():
    product=mongo.db.product.find()
    resp=dumps(product)
    return resp

@app.errordetection(404)
def not_found(error=None):
    message = {
        'status' : 404,
        'message' : 'Not Found' + request.url
    }
    resp = jsonify(messages)
    resp.status_code = 404
    return resp

if __name__=="__main__":
    app.run(debug=True)
