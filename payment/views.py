from portone_server_sdk.payment import PaymentClient

def payment_view():
    return PaymentClient.pay_instantly()