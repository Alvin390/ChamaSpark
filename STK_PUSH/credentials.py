import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64
import os
from django.http import JsonResponse
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Firebase configuration
from decouple import config

FIREBASE_PROJECT_ID = config('FIREBASE_PROJECT_ID')
FIREBASE_PRIVATE_KEY_ID = config('FIREBASE_PRIVATE_KEY_ID')
FIREBASE_PRIVATE_KEY = config('FIREBASE_PRIVATE_KEY').replace('\\n', '\n')
FIREBASE_CLIENT_EMAIL = config('FIREBASE_CLIENT_EMAIL')
FIREBASE_CLIENT_ID = config('FIREBASE_CLIENT_ID')
FIREBASE_AUTH_URI = config('FIREBASE_AUTH_URI')
FIREBASE_TOKEN_URI = config('FIREBASE_TOKEN_URI')
FIREBASE_AUTH_PROVIDER_X509_CERT_URL = config('FIREBASE_AUTH_PROVIDER_X509_CERT_URL')
FIREBASE_CLIENT_X509_CERT_URL = config('FIREBASE_CLIENT_X509_CERT_URL')

class MpesaC2bCredential:
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'


class MpesaAccessToken:
    r = requests.get(MpesaC2bCredential.api_URL,
                     auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]


class LipanaMpesaPpassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = "174379"
    OffSetValue = '0'
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

    data_to_encode = Business_short_code + passkey + lipa_time

    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')

