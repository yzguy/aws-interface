#!/usr/bin/env python

import boto3, pprint

size_mappings = {
    'small': 't2.small',
    'medium': 't2.medium',
    'large': 't2.large'
}

for k,v in size_mappings.items():
    print k
    print v

#ec2 = boto3.client('ec2')
#allowed_amis = ['ami-d0f506b0', 'ami-775e4f16', 'ami-9abea4fb']
#resp = ec2.describe_images(ImageIds=allowed_amis)

#pprint.pprint(resp)
