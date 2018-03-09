from news_recommendation_service import click_log_processor
import os
import sys

from datetime import datetime
# from sets import Set
import parameters

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

from common import AWS_mongodb_client

MONGODB_PREFERENCE_MODEL_TABLE_NAME = parameters.MONGODB_PREFERENCE_MODEL_TABLE_NAME
NEWS_TABLE_NAME = "newCollection"

NUM_OF_CLASSES = 17


# Start MongoDB before running following tests.
def test_basic():
    db = AWS_mongodb_client.get_db()
    db[MONGODB_PREFERENCE_MODEL_TABLE_NAME].delete_many({"userId": "test_user"})

    msg = {"userId": "test_user",
           "newsId": "test_news",
           "timestamp": str(datetime.utcnow())}

    click_log_processor.handle_message(msg)

    model = db[MONGODB_PREFERENCE_MODEL_TABLE_NAME].find_one({'userId':'test_user'})
    assert model is not None
    assert len(model['preference']) == NUM_OF_CLASSES

    print('test_basic passed!')


if __name__ == "__main__":
    test_basic()
