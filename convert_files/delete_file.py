import os
import requests
from requests.auth import HTTPBasicAuth

def delete_file(base_url, file_id):
    try:
        endpoint = f'{base_url}/v1/files/{file_id}'
        res = requests.delete(endpoint, stream=True,
                              auth=HTTPBasicAuth(os.environ.get('API_KEY'), '')).json()
    
        print('Deleted file on remote server')
        print(res)
        return True
    except requests.ConnectionError:
        print('Error deleting file on server')
