import json
import urllib.request
import boto3

#Plaid API Url
url = 'https://sandbox.plaid.com/item/get'

#Secret that holds API keys
secret_name = "plaid-api-sandbox-creds"
region_name = "us-east-1"

#Initialize boto3 + secrets manager
session = boto3.session.Session()
client = session.client(
    service_name = 'secretsmanager',
    region_name = region_name
)

#Retreive API keys
resp = client.get_secret_value(SecretId = secret_name)['SecretString']
api_creds = json.loads(resp)
print(api_creds)
#Parse Secret
access_key = api_creds.get("access_key")
client_id = api_creds.get("client_id")
secret = api_creds.get("secret")

def lambda_handler(event, context):
    
    payload = json.dumps({
        "client_id": client_id,
        "secret": secret,
        "access_token": access_key
    }).encode("utf-8")

    try:
        req = urllib.request.Request(
            url,
            data = payload,
            headers = {"Content-Type": "application/json"},
            method = "POST"
        )

        with urllib.request.urlopen(req) as res:
            raw = res.read()
            data = json.loads(raw.decode("utf-8"))
            return data
    
    except urllib.error.HTTPError as e:
        print(e.read().decode())
        raise
