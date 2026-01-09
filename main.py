from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/payment/callback", methods=["GET", "POST"])
async def razorpay_callback(request: Request):
    params = request.query_params
    print(params)

    razorpay_payment_id = params.get("razorpay_payment_id")
    razorpay_signature = params.get("razorpay_signature")
    razorpay_payment_link_status = params.get("razorpay_payment_link_status")

    if razorpay_payment_link_status != "paid":
        return {"status": "failed"}

    return {"status": "success", "payment_id": razorpay_payment_id}
