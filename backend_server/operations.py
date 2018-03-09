import json
import os
import pickle
import random
import redis
import sys
import time

from bson.json_util import dumps
from datetime import datetime
from kafka import KafkaProducer

# import common package in parent directory
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common import AWS_mongodb_client # defined get_db() that return the db from a certain host:port
from common import news_recommendation_service_client
import parameters

# mongodb
MONGODB_NEWS_TABLE_NAME = parameters.MONGODB_NEWS_TABLE_NAME
MONGODB_CLICK_LOGS_TABLE_NAME = parameters.MONGODB_CLICK_LOGS_TABLE_NAME
MONGODB_NEWS_LIMIT = parameters.MONGODB_NEWS_LIMIT
MONGODB_NEWS_LIST_BATCH_SIZE = parameters.MONGODB_NEWS_LIST_BATCH_SIZE

# redis connect
AWS_REDIS_PORT = parameters.AWS_redisPort
AWS_redis_client = redis.StrictRedis(parameters.AWS_redisHost, AWS_REDIS_PORT, db=0)
REDIS_USER_NEWS_TIME_OUT_IN_SECONDS = parameters.AWS_REDIS_USER_NEWS_TIME_OUT_IN_SECONDS

# Kafka
AWS_Log_kafka_producer = KafkaProducer(bootstrap_servers=parameters.AWS_KAFKA_SERVER)
AWS_KAFKA_LOG_CLICKS_TASK_QUEUE = parameters.AWS_KAFKA_LOG_CLICKS_TASK_QUEUE


def getNewsSummariesForUser(user_id, page_num):

    page_num = int(page_num)
    begin_index = (page_num - 1) * MONGODB_NEWS_LIST_BATCH_SIZE
    end_index = page_num * MONGODB_NEWS_LIST_BATCH_SIZE

    # The final list of news to be returned.
    sliced_news = []

    if AWS_redis_client.get(user_id) is not None:
        news_digests = pickle.loads(AWS_redis_client.get(user_id)) # GET the corresponding (VALUE)news_id by (KEY)a user_id

        # If begin_index is out of range, this will return empty list;
        # If end_index is out of range (begin_index is within the range), this
        # will return all remaining news ids.
        sliced_news_digests = news_digests[begin_index:end_index]
        print(sliced_news_digests)
        db = AWS_mongodb_client.get_db()
        # "newCollection"
        sliced_news = list(db[MONGODB_NEWS_TABLE_NAME].find({'digest':{'$in':sliced_news_digests}}))
    else:
        db = AWS_mongodb_client.get_db()
        # sort in descending order(-1)
        total_news = list(db[MONGODB_NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(MONGODB_NEWS_LIMIT))
        total_news_digests = map(lambda x:x['digest'], total_news)

        AWS_redis_client.set(user_id, pickle.dumps(total_news_digests))
        AWS_redis_client.expire(user_id, REDIS_USER_NEWS_TIME_OUT_IN_SECONDS)

        sliced_news = total_news[begin_index:end_index]

    # Get preference for the user
    preference = news_recommendation_service_client.getPreferenceForUser(user_id)
    topPreference = None

    if preference is not None and len(preference) > 0:
        topPreference = preference[0]

    for news in sliced_news:
        # Remove text field to save bandwidth.
        del news['text']
        if news['class'] == topPreference:
            news['reason'] = 'Recommend'
        if news['publishedAt'].date() == datetime.today().date():
            news['time'] = 'today'
    return json.loads(dumps(sliced_news))


def logNewsClickForUser(user_id, news_id):
    message = {'userId': user_id, 'newsId': news_id, 'timestamp': datetime.utcnow()}

    db = AWS_mongodb_client.get_db()
    # user_id;  newsID; timestamp
    db[MONGODB_CLICK_LOGS_TABLE_NAME].insert(message)

    # Send log task to machine learning service for prediction
    message = {'userId': user_id, 'newsId': news_id}
    AWS_Log_kafka_producer.send(topic=AWS_KAFKA_LOG_CLICKS_TASK_QUEUE,
                                value=json.dumps(message), timestamp_ms=time.time())
