from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import json
from bson.json_util import dumps, loads

def find_docs(db, collection, search=''):
    res = db[collection].find(
        {
            '$or': [{
                'name': {
                    '$regex': search,
                    '$options': 'i'
                }
            }]
        }
    )
    return json.loads(dumps(res))

def get_all(db, collection):
    res = db[collection].find({})
    return json.loads(dumps(res))

load_dotenv()

client = MongoClient(os.environ.get('URI'))
db = client[os.environ.get('DB')]

app = FastAPI()

@app.get('/')
async def root():
    return 'get the bts meal from mcdonalds'

@app.get('/get_all/{collection}')
async def get_all_collection(collection: str):
    try:
        return get_all(db, collection)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/search/{collection}/{name}')
async def search_collection(collection: str, name: str):
    try:
        return find_docs(db, collection, name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
