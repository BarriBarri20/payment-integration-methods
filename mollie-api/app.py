from flask import Flask
import flask

from dotenv import load_dotenv
import os
import time
from mollie.api.client import Client
from mollie.api.error import Error

# Load environment variables from .env file
load_dotenv()

# Access environment variables
flask_app = os.getenv("FLASK_APP")
flask_env = os.getenv("FLASK_ENV")
flask_debug = os.getenv("FLASK_DEBUG")
mollie_api_key = os.getenv("MOLLIE_API_KEY")
mollie_public_url = os.getenv("MOLLIE_PUBLIC_URL")

# Create Flask app
app = Flask(flask_app)


@app.route("/")
def hello():
    return "Hello, World!"


api_key = mollie_api_key

mollie_client = Client()
mollie_client.set_api_key(api_key)


@app.route("/create-payment")
def test():
    print("test")

    #
    # Initialize the Mollie API library with your API key.
    #
    # See: https://www.mollie.com/dashboard/settings/profiles
    #

    #
    mollie_client = Client()
    mollie_client.set_api_key(mollie_api_key)
    payment = mollie_client.payments.create(
        {
            "amount": {
                "currency": "EUR",
                "value": "10.00",
            },
            "description": "Order #12345",
            "redirectUrl": f"https://{mollie_public_url}/payments/webhook/",
            "webhookUrl": f"https://{mollie_public_url}/order/12345/",
            "metadata": {
                "order_id": "12345",
            },
            "method": "creditcard",
        }
    )
    # Iformation of the payment request : POST request
    return flask.redirect(payment.checkout_url)

    print("web hook url : ", payment.webhook_url)


@app.route("/create-customer")
def create_customer():
    global customer_id
    mollie_client = Client()
    mollie_client.set_api_key(api_key)
    try:
        customer = mollie_client.customers.create(
            {
                "name": "John Doe",
                "email": "john.doe@email.com",
                "locale": "nl_NL",
            }
        )

        customer_id = customer.id
        print(customer_id)
        return f"customer id is {customer_id}"

    except Error as err:
        return f"your error is {err}"


@app.route("/create-order")
def create_order():
    """You can pass the data of the order here like requirements and other things"""

    global order_id  # to access the order id in the order function
    mollie_client = Client()
    mollie_client.set_api_key(api_key)
    print(api_key)
    try:
        # Generate a unique webshop order id for this example.
        my_webshop_id = int(time.time())

        order = mollie_client.orders.create(
            {
                "payment" : {
                    "customerId" : customer_id
                },
                
                "amount": {"value": "299.00", "currency": "EUR"},
                "billingAddress": {
                    "streetAndNumber": "Keizersgracht 313",
                    "city": "Amsterdam",
                    "region": "Noord-Holland",
                    "postalCode": "1234AB",
                    "country": "NL",
                    "givenName": "Piet",
                    "familyName": "Mondriaan",
                    "email": "piet@mondriaan.com",
                },

                "shippingAddress": {
                    "streetAndNumber": "Prinsengracht 313",
                    "city": "Haarlem",
                    "region": "Noord-Holland",
                    "postalCode": "5678AB",
                    "country": "NL",
                    "givenName": "Chuck",
                    "familyName": "Norris",
                    "email": "norris@chucknorrisfacts.net",
                },
                "metadata": {
                    "my_webshop_id": str(my_webshop_id),
                    "description": "Lego cars",
                },
                "consumerDateOfBirth": "1958-01-31",
                "locale": "nl_NL",
                "orderNumber": "1337",
                "redirectUrl": f"https://{mollie_public_url}/order-status?my_webshop_id={my_webshop_id}",
                "webhookUrl": f"https://{mollie_public_url}/order-webhook/",
                "lines": [
                    {
                        "type": "physical",
                        "sku": "5702016116977",
                        "name": "LEGO 42083 Bugatti Chiron",
                        "productUrl": "https://shop.lego.com/nl-NL/Bugatti-Chiron-42083",
                        "imageUrl": "https://sh-s7-live-s.legocdn.com/is/image//LEGO/42083_alt1?$main$",
                        "quantity": 1,
                        "vatRate": "21.00",
                        "unitPrice": {"currency": "EUR", "value": "399.00"},
                        "totalAmount": {"currency": "EUR", "value": "299.00"},
                        "discountAmount": {"currency": "EUR", "value": "100.00"},
                        "vatAmount": {"currency": "EUR", "value": "51.89"},
                    },
                ],
            }
        )

        order_id = order.id
        #
        # Send the customer off to complete the order payment.
        #
        return flask.redirect(order.checkout_url)

    except Error as err:
        return f"your error is {err}"


@app.route("/order-status")
def order():
    mollie_client = Client()
    mollie_client.set_api_key(mollie_api_key)

    if "my_webshop_id" not in flask.request.args:
        flask.abort(404, "Unknown webshop id")

    order = mollie_client.orders.get(order_id)

    if order.is_paid():
        return f"The payment for your order {order.id} has been processed"

    elif order.is_canceled():
        return f"Your order {order.id} has been canceled"

    elif order.is_shipping():
        return f"Your order {order.id} is shipping"

    elif order.is_created():
        return f"Your order {order.id} has been created"

    elif order.is_authorized():
        return f"Your order {order.id} is authorized"

    elif order.is_refunded():
        return f"Your order {order.id} has been refunded"

    elif order.is_expired():
        return f"Your order {order.id} has expired"

    elif order.is_completed():
        return f"Your order {order.id} is completed"

    else:
        return f"The status of your order {order.id} is: {order.status}"


@app.route("/order-webhook/<customer_id>", methods=["POST"])
def web_hook(customer_id):
    try:
        #
        # Initialize the Mollie API library with your API key.
        #
        # See: https://www.mollie.com/dashboard/settings/profiles
        #
        mollie_client = Client()
        mollie_client.set_api_key(mollie_api_key)

        #
        # After your webhook has been called with the order ID in its body, you'd like
        # to handle the order's status change. This is how you can do that.
        #
        # See: https://docs.mollie.com/reference/v2/orders-api/get-order
        #

        print("I was called : ", flask.request.form.get("id"))
        print("***** customer id : ", customer_id)
        if "id" not in flask.request.form:
            flask.abort(404, "Unknown order id")

        order_id = flask.request.form["id"]
        order = mollie_client.orders.get(order_id)
        my_webshop_id = order.metadata["my_webshop_id"]
        #
        # Update the order in the database.
        #
        data = {"order_id": order.id, "status": order.status}

        if order.is_paid() or order.is_authorized():
            #
            # At this point you'd probably want to start the process of delivering the product to the customer.
            #
            return "Paid"
        if order.is_canceled():
            #
            # At this point you'd probably want to inform the customer that the order has been canceled.
            #
            return "Canceled"
        if order.is_completed():
            #
            # At this point you could inform the customer that all deliveries to the customer have started.
            #
            return "Completed"

    except Error as err:
        return f"API call failed: {err}"


@app.route("/create_account")
def create_account():
    # when creating a cart create account to customer

    customer = mollie_client.customers.create(
        {
            "name": "Customer A",
            "email": "customer@example.org",
        }
    )


@app.route("/subscribe")
def subscribe():
    cleint_id = get_client_id()
    customer = mollie_client.customers.get(client_id)
    subscription = customer.subscriptions.create(
        {
            "amount": {
                "currency": "EUR",
                "value": "25.00",
            },
            "times": 4,
            "interval": "3 months",
            "description": "Quarterly payment",
            "webhookUrl": "https://webshop.example.org/subscriptions/webhook/",
        }
    )
