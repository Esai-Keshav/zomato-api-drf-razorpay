key_id = "rzp_test_S1fibxSeI091z8"
key_secret = "1q1IetSrDcYSZMPmdzHVLXuk"

import razorpay


client = razorpay.Client(auth=(key_id, key_secret))

res = client.payment_link.create(
    {
        "amount": 500 * 100,
        "currency": "INR",
        "description": "For DRF",
        "customer": {
            "name": "Gaurav Kumar",
            "email": "gaurav.kumar@example.com",
            "contact": "+919876543210",
        },
        "notify": {"sms": True, "email": True},
        "reminder_enable": True,
        "notes": {"policy_name": "Cyces "},
        "callback_url": "http://localhost:8000/api/payment/callback/",
        "callback_method": "get",
    }
)

# print(res["short_url"])
# print(res)

payment_id = "pay_S1jV7rlBk3Nvc7"
payment = client.payment.fetch(payment_id)

print(payment)
# card 2305 3242 5784 8228
