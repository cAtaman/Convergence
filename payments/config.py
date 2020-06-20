import os

base_dir = os.path.dirname(__file__)
base_url = 'https://api.wallets.africa/'
base_url_sandbox = 'https://sandbox.wallets.africa/'

PUBLIC_KEY = os.environ['WALLET_API_PUBLIC_KEY']
SECRET_KEY = os.environ['WALLET_API_SECRET_KEY']

PUBLIC_KEY_SANDBOX = "uvjqzm5xl6bw"
SECRET_KEY_SANDBOX = "hfucj5jatq8h"

master_details = {
                     "secret_key": SECRET_KEY,
                     "provider_code": 'etisalat',
                     "amount": 100,
                     "phone_number": '08097829320',
                     "bvn": "22409903043",
                     "date_of_birth": "06-04-1998",
                  }
