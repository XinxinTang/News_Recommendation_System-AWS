from kafka.producer import KafkaProducer
from kafka.errors import KafkaError, KafkaTimeoutError
import datetime
import hashlib
import os
import redis
import sys
import json
import time

# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import parameters
from common import news_api_client

NEWS_SOURCES = [
    'bbc-news',
    'bbc-sport',
    'bloomberg',
    'cnn',
    'entertainment-weekly',
    'espn',
    'ign',
    'techcrunch',
    'the-new-york-times',
    'the-wall-street-journal',
    'the-washington-post'
]

# AWS_redisHost = 'ec2-52-205-251-116.compute-1.amazonaws.com'; AWS_redisPort = 6380
AWS_redis_client = redis.StrictRedis(parameters.AWS_redisHost, parameters.AWS_redisPort)

# AWS_KAFKA_SERVER = ['ec2-54-163-153-215.compute-1.amazonaws.com:9092', 'ec2-52-207-212-20.compute-1.amazonaws.com:9092']
Scrape_AWS_kafka_producer = KafkaProducer(bootstrap_servers=parameters.AWS_KAFKA_SERVER)

while True:
    news_list = news_api_client.getNewsFromSource(NEWS_SOURCES)

    num_of_new_news = 0
    print(len(news_list))
    for news in news_list:
        # extract content of title to news_digest
        news_digest = hashlib.md5(news['title'].encode('utf-8')).digest().encode('base64')

        if AWS_redis_client.get(news_digest) is None:
            num_of_new_news += 1
            news['digest'] = news_digest

            if news['publishedAt'] is None:
                # format: YYYY-MM-DDTHH:MM:SSZ in UTC
                news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

            AWS_redis_client.set(news_digest, news)
            AWS_redis_client.expire(news_digest, parameters.AWS_REDIS_NEWS_TIME_OUT_IN_SECONDS)  # one day
            Scrape_AWS_kafka_producer.send(topic=parameters.AWS_KAFKA_SCRAPE_NEWS_TASK_QUEUE,
                                           value=json.dumps(news), timestamp_ms=time.time())

    print("Fetched {} new news.".format(num_of_new_news))
    time.sleep(parameters.SLEEP_TIME_IN_SECONDS)
