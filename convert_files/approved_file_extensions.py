import os
import requests
from requests.auth import HTTPBasicAuth

def approved_file_extensions(base_url, file_format):
    try:
        endpoint = '{}/v1/formats/{}'.format(base_url, file_format)
        res = requests.get(endpoint, auth=HTTPBasicAuth(os.environ.get('API_KEY'), '')).json()
        if 'errors' in res:
            return False
        
        return {target['name'] for target in res['targets']}
    
    except requests.ConnectionError as error:
        print(error)
        
