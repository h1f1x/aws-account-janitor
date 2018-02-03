import boto3
from .logging import log


def get_log_groups():
    client = boto3.client('logs')
    attrs = {}
    log_groups = []
    while True:
        result = client.describe_log_groups(**attrs)
        log_groups.extend(result['logGroups'])
        if 'nextToken' not in result:
            break
        attrs['nextToken'] = result['nextToken']
    return log_groups


def get_log_groups_wo_retention():
    return [g for g in get_log_groups() if 'retentionInDays' not in g]


def set_retention_for_missing(days=7):
    client = boto3.client('logs')
    for group in get_log_groups_wo_retention():
        log('Setting retention to {} days for: {}'.format(days, group['logGroupName']))
        client.put_retention_policy(logGroupName=group['logGroupName'], retentionInDays=days)
