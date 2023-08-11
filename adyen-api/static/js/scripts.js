const clientKey = JSON.parse(document.getElementById('client-key').innerHTML);
const session = JSON.parse(JSON.parse(document.getElementById('session').innerHTML));

async function initCheckout() {

    try {
        const checkout = await createAdyenCheckout(session, clientKey);
        console.log(checkout);

        const dropin = checkout.create('dropin').mount('#dropin-container');
        console.log(dropin);
    } catch (error) {
        console.error(error);
    }
}


async function createAdyenCheckout(session, clientKey) {



    const configuration = {
        clientKey,
        locale: "en_US",
        environment: "test",  // change to live for production
        showPayButton: true,
        session: session,
        paymentMethodsConfiguration: {
            ideal: {
                showImage: true
            },
            card: {
                hasHolderName: true,
                holderNameRequired: true,
                name: "Credit or debit card",
                amount: {
                    value: session.amount.value,
                    currency: session.amount.currency
                }
            },
            paypal: {
                amount: {
                    value: session.amount.value,
                    currency: session.amount.currency
                },
                environment: "test",
                countryCode: "US"   // Only needed for test. This will be automatically retrieved when you are in production.
            }
        },

        onPaymentCompleted: (result, component) => {
            handleServerResponse(result, component);
        },
        onError: (error, component) => {
            console.error(error.name, error.message, error.stack, component);
        }
    };
    return new AdyenCheckout(configuration);
}


// Handles responses sent from your server to the client
function handleServerResponse(res, component) {
    if (res.action) {
        component.handleAction(res.action);
    } else {
        switch (res.resultCode) {
            case "Authorised":
                window.location.href = "/result/success";
                break;
            case "Pending":
            case "Received":
                window.location.href = "/result/pending";
                break;
            case "Refused":
                window.location.href = "/result/failed";
                break;
            default:
                window.location.href = "/result/error";
                break;
        }
    }
}

initCheckout();