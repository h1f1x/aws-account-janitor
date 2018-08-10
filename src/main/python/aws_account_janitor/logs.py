import boto3
import time
from .logging import log


def list_log_groups():
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


def list_log_groups_wo_retention():
    return [g for g in list_log_groups() if 'retentionInDays' not in g]


def get_last_event_time(log_group_name):
    client = boto3.client('logs')
    response = client.describe_log_streams(
                logGroupName=log_group_name,
                orderBy='LastEventTime',
                descending=True,
                limit=1)
    if not len(response['logStreams']):
        return None
    return response['logStreams'][0].get('lastEventTimestamp')


def list_not_used_log_groups(multiplier=2):
    '''
    List log groups with last event happened before:
    muliplier * retention time (default double the retention time)
    If a log group has not set a retention time it will not be listed.
    '''
    log_groups = list_log_groups()
    result = []
    now = get_time_in_millis()
    for group in log_groups:
        orphan = False
        if 'retentionInDays' not in group:
            continue
        last_event_time = get_last_event_time(group['logGroupName'])
        if not last_event_time:
            orphan = True
        else:
            offset = multiplier * get_offset(group['retentionInDays'])
            if last_event_time + offset < now:
                orphan = True
        if orphan:
            result.append(group)
    return result


def get_offset(days):
    return days * 24 * 60 * 60 * 1000


def get_time_in_millis():
    return int(round(time.time() * 1000))


def set_retention_for_missing(days=7):
    client = boto3.client('logs')
    for group in list_log_groups_wo_retention():
        log('Setting retention to {} days for: {}'.format(days, group['logGroupName']))
        client.put_retention_policy(logGroupName=group['logGroupName'], retentionInDays=days)
