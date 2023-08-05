from flask import Flask

from dotenv import load_dotenv
import os
import time
from mollie.api.client import Client
from mollie.api.error import Error

# Load environment variables from .env file
load_dotenv()

# Access environment variables
flask_app = os.getenv('FLASK_APP')
flask_env = os.getenv('FLASK_ENV')
flask_debug = os.getenv('FLASK_DEBUG')
mollie_api_key = os.getenv('MOLLIE_API_KEY')
mollie_public_url = os.getenv('MOLLIE_PUBLIC_URL')

# Create Flask app
app = Flask(flask_app)

@app.route('/')
def hello():
    return 'Hello, World!'



def test():
    print('test')

    #
    # Initialize the Mollie API library with your API key.
    #
    # See: https://www.mollie.com/dashboard/settings/profiles
    #
    api_key = os.environ.get(mollie_api_key, "test_test")
    mollie_client = Client()
    mollie_client.set_api_key(api_key)

    #
    mollie_client = Client()
    mollie_client.set_api_key(mollie_api_key)
    payment = mollie_client.payments.create({
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
    })
    # Iformation of the payment request : POST request
    print(payment.checkout_url)
    print('web hook url : ', payment.webhook_url)




@app.route('/order/<order_id>')
def order(order_id):

        mollie_client = Client()
        order_id = flask.request.form["id"]
        order = mollie_client.orders.get(order_id)
        my_webshop_id = order.metadata["my_webshop_id"]

        if payment.is_paid():
            #
            # At this point you'd probably want to start the process of delivering the product to the customer.
            #
            status = "Paid"

    return f'Order: {order_id} - {time.time()} & the status of the order : {status}'
