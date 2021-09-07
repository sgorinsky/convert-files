import os
import requests
from requests.auth import HTTPBasicAuth

def download_file(base_url, target_file, output_dir):
    try:
        endpoint = '{}/v1/files/{}/content'.format(base_url, target_file['id'])
        res = requests.get(endpoint, stream=True,
                           auth=HTTPBasicAuth(os.environ.get('API_KEY'), ''))
        output_path = '{}/{}'.format(output_dir, target_file['name'])
        with open(output_path, 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()

        return output_path

    except (IOError, requests.ConnectionError) as error:
        print(error)
        return False
