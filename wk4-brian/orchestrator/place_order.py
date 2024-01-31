from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

book_URL = "http://book:5000/book"
order_URL = "http://order:5001/order"
shipping_record_URL = "http://shipping_record:5002/shipping_record"
activity_log_URL = "http://activity:5003/activity_log"
error_URL = "http://error:5004/error"


@app.route("/place_order", methods=["POST"])
def place_order():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            order = request.get_json()
            print("\nReceived an order in JSON:", order)

            # do the actual work
            # 1. Send order info {cart items}
            result = processPlaceOrder(order)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = (
                str(e)
                + " at "
                + str(exc_type)
                + ": "
                + fname
                + ": line "
                + str(exc_tb.tb_lineno)
            )
            print(ex_str)

            return (
                jsonify(
                    {"code": 500, "message": "place_order.py internal error: " + ex_str}
                ),
                500,
            )

    # if reached here, not a JSON request.
    return (
        jsonify(
            {"code": 400, "message": "Invalid JSON input: " + str(request.get_data())}
        ),
        400,
    )


def processPlaceOrder(order):
    # 2. Send the order info {cart items}
    # Invoke the order microservice
    print("\n-----Invoking the order microservice-----")
    order_result = invoke_http(order_URL, method="POST", json=order)
    print("order_result:", order_result)
    # 4. Record new order
    # record the activity log anyway
    print("\n-----Invoking the activity log microservice-----")
    activity_log_result = invoke_http(
        activity_log_URL, method="POST", json=order_result
    )
    print("activity_log_result:", activity_log_result)

    # Check the order result; if a failure, send it to the error microservice.
    print("LOGIC to check if the order has failed!")
    if order_result["code"] not in range(200, 300):
        print("Order failed! - Sending to error microservice")
        # Inform the error microservice
        error_result = invoke_http(error_URL, method="POST", json=order_result)
        print("Error! in order creation:", error_result)
        # 7. Return error
        return {
            "code": 500,
            "data": {"order_result": order_result, "shipping_result": shipping_result},
            "message": "Order failed!",
        }

    # 5. Send new order to shipping
    print("\n-----Invoking the shipping microservice-----")
    shipping_result = invoke_http(
        shipping_record_URL, method="POST", json=order_result["data"]
    )
    print("shipping_result:", shipping_result)
    if shipping_result["code"] not in range(200, 300):
        print("Shipping failed! - sending to error MS again")
        error_result = invoke_http(error_URL, method="POST", json=shipping_result)
        print("Error in order to shipping!:", error_result)

        # Check the shipping result;
        # if a failure, send it to the error microservice.

        # Inform the error microservice

        # 7. Return error
        return {
            "code": 500,
            "data": {"order_result": order_result, "shipping_result": shipping_result},
            "message": "Shipping Order failed!",
        }
    # 7. Return created order, shipping record
    return {
        "code": 201,
        "data": {
            "order_result": order_result,
            "shipping_result": shipping_result,
        },
    }


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program,
    #       and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
