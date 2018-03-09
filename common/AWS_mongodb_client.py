from pymongo import MongoClient
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import parameters

AWS_MONGO_DB_HOST = parameters.AWS_MONGO_DB_HOST
AWS_MONGO_DB_PORT = parameters.AWS_MONGO_DB_PORT
AWS_DB_NAME = parameters.AWS_DB_NAME

AWS_MONGODB_client = MongoClient("{}:{}".format(AWS_MONGO_DB_HOST, AWS_MONGO_DB_PORT))


def get_db(db = AWS_DB_NAME):
    db = AWS_MONGODB_client[db]
    return db
