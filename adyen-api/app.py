from flask import Flask
import flask, json

from dotenv import load_dotenv
import os
import time

# Load environment variables from .env file
load_dotenv()

from Adyen.util import is_valid_hmac_notification
from .sessions import adyen_sessions

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if flask.request.method == "POST":
        total_price = 0

        for i in flask.request.form.keys():
            print(i)

        return f"Total price: //{total_price}"
    return flask.render_template("index.html")


@app.route("/cart", methods=["GET", "POST"])
def cart():
    items = {
        "item-1": {
            "name": "Item 1",
            "price": 100,
            "quantity": 1,
        },
        "item-2": {
            "name": "Item 2",
            "price": 200,
            "quantity": 3,
        },
        "item-3": {
            "name": "Item 3",
            "price": 300,
            "quantity": 2,
        },
    }
    if flask.request.method == "POST":
        order_price = 0
        for item_id in flask.request.form.keys():
            order_price += items[item_id]["price"] * int(flask.request.form[item_id])

        # Create order and associate the customer, price, date of purchase and all related information

        order = {"price": order_price, "purchased_at": time.time()}

        # https://docs.adyen.com/online-payments/build-your-integration/additional-use-cases/#sessions-flow-a-single-api-request

        # Create a session for the order
        session_id = adyen_sessions.create_session(order)

        return f"Order price: {order_price}"

    return flask.render_template("cart.html", items=items)


@app.route("/submit-items", methods=["POST", "GET"])
def submit_items():
    request = flask.request
    if request.method == "POST":
        total_price = 0

        for i in request.form.keys():
            print(i)

        return f"Total price: {total_price}"
    else:
        return "Error ea"
