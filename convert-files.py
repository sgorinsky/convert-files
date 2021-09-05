'''
Script for converting different filetypes using the zamzar api
to specified output file format
'''

import os
import time
import requests
from requests.auth import HTTPBasicAuth

api_key = os.environ.get('API_KEY')
source_path = '/Users/samgorinsky/documents/knowledge'
output_path = f'{source_path}/tmp'

# endpoint = 'https://sandbox.zamzar.com/v1/formats/png'
# response = requests.get(endpoint, auth=HTTPBasicAuth(api_key, ''))
# print(response.json())

# sample
def create_job(job_endpoint, source_file, target_format):
    file_content = {'source_file': open(source_file, 'rb')}
    data_content = {'target_format': target_format}
    res = requests.post(endpoint, data=data_content, files=file_content, auth=HTTPBasicAuth(api_key, ''))
    print('Created job')
    print(res.json())
    return res.json()

def check_if_done(job_id):
    endpoint = f'https://sandbox.zamzar.com/v1/jobs/{job_id}'
    res = requests.get(endpoint, auth=HTTPBasicAuth(api_key, ''))
    json_response = res.json()
    print(json_response)
    return True if json_response['finished_at'] else False

def download_file(job_id, output_path):
        endpoint = 'https://sandbox.zamzar.com/v1/files/{}/content'.format(job_id)
        response = requests.get(endpoint, stream=True, auth=HTTPBasicAuth(api_key, ''))
        if not response.json()['errors']:
            try:
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            f.flush()

                    print('File downloaded')
                    delete_file(job_id)

            except IOError:
                print('Error')
        else:
            print(f'Errors {response.json()}')
            
def delete_file(job_id):
    endpoint = 'https://sandbox.zamzar.com/v1/files/{}/content'.format(job_id)
    response = requests.delete(endpoint, stream=True,
                               auth=HTTPBasicAuth(api_key, ''))
    print('Deleted file')
    print(res.json())
    

# endpoint = 'https://sandbox.zamzar.com/v1/jobs'
# source_file = 'example.png'
# target_format = 'jpg'

# job = create_job(endpoint, source_file, target_format)
# while not check_if_done(job['id']):
#     time.sleep(1)

download_file(110915097, 'tmp/example.jpg')
    
