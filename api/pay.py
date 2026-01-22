key_id = "rzp_test_S1fibxSeI091z8"
key_secret = "1q1IetSrDcYSZMPmdzHVLXuk"

import razorpay

client = razorpay.Client(auth=(key_id, key_secret))


def get_url(amount=200, order_id=1):
    res = client.payment_link.create(
        {
            "amount": amount * 100,
            "currency": "INR",
            "description": "For DRF",
            "customer": {
                "name": "Gaurav Kumar",
                "email": "gaurav.kumar@example.com",
                "contact": "+919876543210",
            },
            "notify": {"sms": True, "email": True},
            "reminder_enable": True,
            "notes": {"order_id": order_id},
            # "callback_url": "http://localhost:8000/api/payment/callback/",
            "callback_url": "http://localhost:5173/orders/",
            "callback_method": "get",
        }
    )

    print(res)
    return {"pay_url": res["short_url"]}


# card 2305 3242 5784 8228


def payment_status(payment_id):
    # payment_id = "pay_S1jV7rlBk3Nvc7"
    payment = client.payment.fetch(payment_id)

    return payment
