import os
import requests
from requests.auth import HTTPBasicAuth

def create_job(base_url, source_file, target_format):
    try:
        endpoint = f'{base_url}/v1/jobs'
        file_content = {'source_file': open(source_file, 'rb')}
        data_content = {'target_format': target_format}
        res = requests.post(endpoint, data=data_content,
                            files=file_content, auth=HTTPBasicAuth(os.environ.get('API_KEY'), '')).json()
        
        print('Job {} for {} created'.format(res['id'], res['name']))
        return res
    
    except requests.ConnectionError:
        print('Issue requesting server to create job for {}'.format(source_file))
        return False
        
