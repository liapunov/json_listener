# -*- coding: utf-8 -*-
"""
Created on Mon May 11 22:55:48 2020

@author: frina
"""

#import logging as log
from flask import Flask, request
from importlib import import_module
from utils.cognito import CognitoParser


subscriptions = {
    "cognito": {
        "zoom": {
            "module": ".zoom",
            "handler": "ZoomWebinar"
            }
        }
    }


#log.basicConfig(filename="webhook.log",
#                level=log.DEBUG,
#                format='%(asctime)s - %(levelname)s - %(message)s')
#logger = log.getLogger("Webhook")


app = Flask(__name__)


def shutdown_server():
    """
    Shut down the webhook.

    Raises:
        RuntimeError: If the Werkzeug server is not running properly.

    """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def dispatch_form(source, meta=None, payload=None):
    """Call the receivers' form handlers."""
    if source in subscriptions.keys():
        for subscriber in subscriptions[source].keys():
            module = subscriptions[source][subscriber]["module"]
            handler = subscriptions[source][subscriber]["handler"]
            module = import_module(module, package="utils")
            subscriber_class = getattr(module, handler)
            subscriber_class(meta, payload)


@app.route('/', methods=['GET'])
def index():
    """Parse the incoming request and calls the appropriate method."""
    # log.info("receiving a post request from cognitoforms...", flush=True)
    base = "ICCJ webhook v1.0"
    raw = str(request.__dict__)
    response = "\n".join([base, raw])
    # log.info(response)
    return (response, 200, None)


@app.route('/cognito', methods=['POST'])
def handle_cognito_form():
    """Parse the post request from Cognito Forms."""
    parser = CognitoParser(request.data)
    meta, payload = parser.get_data()
    print(payload)
    dispatch_form("cognito", meta, payload)
    return (str(payload), 200, None)


@app.route('/shutdown', methods=['POST'])
def shutdown():
    """Get the webhook shutdown request."""
    shutdown_server()
    return 'Server shutting down...'


if __name__ == "__main__":
	app.run(debug=False)