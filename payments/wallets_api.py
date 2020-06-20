import requests
import json
from payments.config import base_url
from payments.config import PUBLIC_KEY, SECRET_KEY

# requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"
headers = {
           'Content-Type': 'application/json',
           'Authorization': 'Bearer ' + PUBLIC_KEY,
           }


def airtime_recharge(phone_number, amount, provider_code):
    url = base_url + '/bills/airtime/purchase'
    payload = {
               "Code": provider_code,
               "Amount": amount,
               "PhoneNumber": phone_number,
               "SecretKey": SECRET_KEY,
               }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    return json.loads(response.text)


def resolve_bvn_self(bvn, date_of_birth):
    payload = {
        "bvn": bvn,
        "dateOfBirth": date_of_birth,
        "SecretKey": SECRET_KEY,
    }
#
