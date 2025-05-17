import requests

API_KEY = "6ceac5d5-4430-4915-b52e-52c589fa52ee.aaec4162-676f-4bc4-938a-cafafe7bba39"
BASE_URL = "http://api.payamakapi.ir/api/v1/SMS/SmartOTP"


def send_otp_message(number, code):
    message_template = f"""
    کاربر گرامی کد زیر برای ورد به پنل کاربری می‌باشد.
    رمز ورود شما : {code}
    asr-elevator.ir
    """
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    time = "5"

    payload = {
        "ToNumber": number,
        "Content": message_template,
    }

    request = requests.post(BASE_URL, headers=headers, json=payload)
    return request.json()


