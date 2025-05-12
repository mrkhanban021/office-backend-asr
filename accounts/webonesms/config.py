import requests

API_KEY = "6ceac5d5-4430-4915-b52e-52c589fa52ee.aaec4162-676f-4bc4-938a-cafafe7bba39"
BASE_URL = "http://api.payamakapi.ir/api/v1/SMS/SmartOTP"


def send_otp_message(number, code):
    # message = f"کاربر گرامی کد زیر برای ورود به پنل کاربری می‌باشد.\nرمز ورود شما : {code}\nasr-elevator.ir"
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    time = "5"

    payload = {
        "ToNumber": number,
        "Content": f"رمز یک بار مصرف شما:{code} مدت اعتبار  {time} asr-elevator.ir"
    }

    request = requests.post(BASE_URL, headers=headers, json=payload)
    print(request.status_code)
    print(request.json())


