#!/usr/bin/env python
import sys
import boto3
import argparse
from botocore.exceptions import ClientError

parser = argparse.ArgumentParser(description='Report on Groups')
parser.add_argument('--profile', help='AWS profile', default='default')
parser.add_argument('--region', help="AWS region", default='eu-central-1')
args = parser.parse_args()

session = boto3.Session(profile_name=args.profile, region_name=args.region)
iam = session.client('iam')

try:
    # get groups
    resp = iam.list_groups()
    for group_meta in resp['Groups']:
        print(group_meta['GroupName'] + ':')
        resp2 = iam.get_group(GroupName=group_meta['GroupName'])
        print('  Users:')
        for user in resp2['Users']:
        # output users for groups
            print('    ' + user['UserName'])
        resp3 = iam.list_attached_group_policies(GroupName=group_meta['GroupName'])
        print('  AttachedPolicies:')
        for policy in resp3['AttachedPolicies']:
            print('    ' + policy['PolicyName'])

    # output attached polices for groups

except ClientError as e:
    print("Client Error Exception:", e)
    exit(1)
except Exception as e:
    print("An Exception was caught:")
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print(exc_type, 'line:', exc_tb.tb_lineno, e)
    print(repr(e))
    exit(1)

exit(0)
