from __future__ import print_function

import os
import json
import subprocess
import boto3

print('Loading function')


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    client = boto3.client('s3')
	
    ZAP_OR_TVG = os.environ['ZAP_OR_TVG']
    FILE_NAME = os.environ['FILE_NAME']
    BUCKET_NAME = os.environ['BUCKET_NAME']
    
    if 'ZAP_OR_TVG' in event:
        ZAP_OR_TVG = event['ZAP_OR_TVG']
        
    if 'FILE_NAME' in event:
        FILE_NAME = event['FILE_NAME']
    
    args = ['perl', '-I', 'lib', 'zap2xml.pl' ]

    if ZAP_OR_TVG == 'TVG':
        args.append('-z')
        args.extend(('-u', os.environ['TVG_USERNAME']))
        args.extend(('-p', os.environ['TVG_PASSWORD']))
    else:
        args.extend(('-u', os.environ['ZAP_USERNAME']))
        args.extend(('-p', os.environ['ZAP_PASSWORD']))
    
    args.extend(('-c', '/tmp/cache'))
    args.extend(('-o', '/tmp/%s' % FILE_NAME))
	
    proc = subprocess.Popen(args,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                            )
    stdout_value, stderr_value = proc.communicate()
    print('Output:'  + stdout_value + stderr_value);
	
    client.upload_file('/tmp/%s' % FILE_NAME, BUCKET_NAME, FILE_NAME)