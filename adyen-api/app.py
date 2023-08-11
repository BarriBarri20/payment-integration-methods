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

        host_url = flask.request.host_url

        print("*" * 100)
        print(host_url)

        order = {
            "reference": "order-1",
            "amount": {"value": order_price, "currency": "EUR"},
            "returnUrl": f"{host_url}checkout?shopperOrder=order-1",
            "merchantAccount": os.getenv("ADYEN_MERCHANT_ACCOUNT"),
        }

        # ...
        # save the order in the database
        # ...

        # https://docs.adyen.com/online-payments/build-your-integration/additional-use-cases/#sessions-flow-a-single-api-request

        # Create a session for the order
        session = adyen_sessions(order)

        return flask.render_template(
            "payment.html",
            session=session,
            client_key=os.getenv("ADYEN_CLIENT_KEY"),
        )

    return flask.render_template("cart.html", items=items)


@app.route("/checkout", methods=["POST", "GET"])
def submit_items():
    request = flask.request
    if request.method == "POST":
        total_price = 0

        for i in request.form.keys():
            print(i)

        return f"Total price: {total_price}"
    else:
        return "Error ea"


@app.route("/result/<result>")
def payment(result):
    return flask.render_template("result.html", result=result)
    