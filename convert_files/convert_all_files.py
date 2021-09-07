'''
Script for converting different filetypes using the zamzar api
to specified output file format
'''

import os
import sys
import time
import requests
from requests.auth import HTTPBasicAuth

from create_job import create_job
from is_job_done import is_job_done
from download_file import download_file
from delete_file import delete_file

# Constants
MB = 1024 * 1024
TEST_BASE_URL = 'https://sandbox.zamzar.com'
PROD_BASE_URL = 'https://api.zamzar.com'

source_path = input('Provide source path for files to convert: ') if len(sys.argv) < 2 else sys.argv[1]
output_dir = '{}/conversion_output'.format(os.getcwd() if os.path.isfile(source_path) else source_path)
target_format = input('Target format for files: ') if len(sys.argv) < 3 else sys.argv[2]

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

def walk_dir(source_path):
    if os.path.isfile(source_path):
        create_job_and_download_file(source_path)
        return
    
    for dir, _, files in os.walk(source_path):
        for file in files:
            full_path = '{}/{}'.format(source_path, file)
            if os.path.isdir(full_path):
                walk_dir(full_path)
            else:
                create_job_and_download_file(full_path)
            
            
def create_job_and_download_file(source_path):
    base_url = TEST_BASE_URL if os.path.getsize(source_path) < MB - 20000 else PROD_BASE_URL
    job = create_job(base_url, source_path, target_format)
    checked_job = is_job_done(base_url, job['id'])
    while not checked_job:
        time.sleep(1)
        checked_job = is_job_done(base_url, job['id'])

    target_file = checked_job['target_files'][0]
    print('Target files')
    print(checked_job['target_files'][0])
    download_file(base_url, target_file, output_dir)
    delete_file(base_url, target_file['id'])
    
create_job_and_download_file(source_path)
    
