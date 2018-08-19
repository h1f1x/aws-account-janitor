import boto3

client = boto3.client('resourcegroupstaggingapi')


def get(tag_filters):
    response = client.get_resources(
        TagFilters=tag_filters
    )
    return response


def human_readable(raw_get_resources_response):
    return [
        {**split_resource_arn(e['ResourceARN']), **{'Tags': collapse_tags(e['Tags'])}}
        for e in raw_get_resources_response['ResourceTagMappingList']]


def split_resource_arn(arn):
    _arn = arn.split(':')
    if len(_arn) > 6:
        resource = _arn[5:]
    else:
        resource = _arn[5]
        resource = resource.split('/')
    return {
        'service': _arn[2],
        'region': _arn[3],
        'account_id': _arn[4],
        'name': resource[0],
        'id': resource[1] if len(resource) > 1 else '',
        'arn': arn
        }


def collapse_tags(raw_tags):
    return [(e['Key'], e['Value']) for e in raw_tags]
