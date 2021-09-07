'''
Script for converting different filetypes using the zamzar api
to specified output file format
'''

import os
import sys
import time
import requests
from requests.auth import HTTPBasicAuth

from approved_file_extensions import approved_file_extensions
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

preexisting_files = {
    '{}/{}'.format(output_dir, file.split('.')[0]) \
        for dir, _, files in os.walk(output_dir) \
            for file in files
}

def walk_dir(source_path):
    if os.path.isfile(source_path):
        create_job_and_download_file(source_path)
        return
    
    for dir, _, files in os.walk(source_path):
        for file in files:
            file_no_extension = '{}/{}'.format(output_dir, file.split('.')[0])
            if file == 'conversion_output' or file_no_extension in preexisting_files:
                continue
            
            full_path = '{}/{}'.format(dir, file)
            walk_dir(full_path)
            
            
def create_job_and_download_file(source_path, retry_count=1):
    if os.path.getsize(source_path) > MB:
        return
    
    base_url = TEST_BASE_URL
    print(source_path)
    file_extension = source_path.split('.')[-1]
    if not approved_file_extensions(base_url, file_extension):
        print('No endpoint for {} extension: {}'.format(file_extension, source_path))
        return
        
    created_job = create_job(base_url, source_path, target_format)
    if 'errors' in created_job:
        print('Job failed: {}'.format(created_job))
        return
    
    checked_job = is_job_done(base_url, created_job['id'])
    while checked_job['status'] != 'successful':
        time.sleep(5)
        checked_job = is_job_done(base_url, created_job['id'])
        if checked_job['status'] == 'failed':
            if retry_count > 5:
                print('Max retries exceeded')
                return

            print('Retry count: {}'.format(retry_count))
            return create_job_and_download_file(source_path, retry_count + 1)

    target_file = checked_job['target_files'][0]
    output_file_path = download_file(base_url, target_file, output_dir)
    if output_file_path:
        print('Newly converted file at: {}'.format(output_file_path))
    
    delete_file(base_url, target_file['id'])
    
walk_dir(source_path)
    
