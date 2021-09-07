import os
import requests
from requests.auth import HTTPBasicAuth

def is_job_done(base_url, job_id):
    try:
        endpoint = f'{base_url}/v1/jobs/{job_id}'
        res = requests.get(endpoint, auth=HTTPBasicAuth(os.environ.get('API_KEY'), '')).json()
        
        print('Is job done?')
        print(res)
        return res if res['status'] == 'successful' else False
    except requests.ConnectionError:
        print('Error connecting to endpoint')
