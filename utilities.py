import time
import jwt
import json
import requests
import urllib

def get_id_token(service_account_credential_file, run_service_url):

    # Load service account credentials to dictionary
    with open(service_account_credential_file) as json_file:  
        credentials_json = json.load(json_file)

    # Create and return a signed JWT token to the designated service endpoint
    def create_signed_jwt():
        iat = time.time()
        exp = iat + 3600
        payload = {
            'iss': credentials_json['client_email'],
            'sub': credentials_json['client_email'],
            'target_audience': run_service_url,
            'aud': 'https://www.googleapis.com/oauth2/v4/token',
            'iat': iat,
            'exp': exp
            }
        additional_headers = {
            'kid': credentials_json['private_key_id']
            }
        signed_jwt = jwt.encode(
            payload, 
            credentials_json['private_key'], 
            headers=additional_headers,
            algorithm='RS256'
            )
        return signed_jwt

    # Exchange JWT token for a google-signed OIDC token
    def exchange_jwt_for_token(signed_jwt):
        body = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'assertion': signed_jwt
        }
        token_request = requests.post(
            url = 'https://www.googleapis.com/oauth2/v4/token',
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data = urllib.parse.urlencode(body)
        )
        return token_request.json()['id_token']
    
    # Main
    return exchange_jwt_for_token(create_signed_jwt())