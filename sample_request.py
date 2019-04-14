import utilities 
import requests
import json
import os

CREDENTIAL_FILE = os.getenv('CREDS')
RUN_SERVICE_URL = os.getenv('CLOUD_RUN_SERVICE_URL')

token = utilities.get_id_token(CREDENTIAL_FILE, RUN_SERVICE_URL)
request = requests.get(
    url = RUN_SERVICE_URL,
    headers = {
        'Authorization': f'Bearer {token}'
    }
)
results = {
    'status_code': request.status_code,
    'response': request.json()
}

print(json.dumps(results, indent=2))