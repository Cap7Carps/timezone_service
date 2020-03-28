from timezone_service.greeting import GreetingClient
from timezone_service.errors import InvalidRequestError

from flask import Flask, request


app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    try:
        greeting = GreetingClient(request).run()
        return greeting, 200
    except InvalidRequestError as e:
        return str(e), 400

