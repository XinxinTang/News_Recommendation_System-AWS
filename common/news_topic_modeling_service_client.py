import pyjsonrpc
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import parameters

URL = "http://" + parameters.AWS_RPC_SERVER_HOST + ":6060/"

client = pyjsonrpc.HttpClient(url=URL)


def classify(text):
    topic = client.call('classify', text)
    print("Topic: {}".format(str(topic)))
    return topic
