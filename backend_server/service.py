from backend_server import operations
import pyjsonrpc
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import parameters

AWS_RPC_SERVER_HOST = parameters.AWS_RPC_SERVER_HOST
AWS_RPC_Service_SERVER_PORT = parameters.AWS_RPC_Service_SERVER_PORT


class RequestHandler(pyjsonrpc.HttpRequestHandler):
    """ Test method """
    @pyjsonrpc.rpcmethod
    def add(self, a, b):
        print("add is called with {} and {}".format(a, b))
        return a + b

    """ Get news summaries for a user """
    @pyjsonrpc.rpcmethod
    def getNewsSummariesForUser(self, user_id, page_num):
        return operations.getNewsSummariesForUser(user_id, page_num)

    """ Log user news clicks """
    @pyjsonrpc.rpcmethod
    def logNewsClickForUser(self, user_id, news_id):
        return operations.logNewsClickForUser(user_id, news_id)


# Threading HTTP Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address=(AWS_RPC_SERVER_HOST, AWS_RPC_Service_SERVER_PORT),
    RequestHandlerClass=RequestHandler
)

print("Starting HTTP server on {}:{}".format(AWS_RPC_SERVER_HOST, AWS_RPC_Service_SERVER_PORT))

http_server.serve_forever()
