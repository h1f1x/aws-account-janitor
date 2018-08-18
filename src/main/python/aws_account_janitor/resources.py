import boto3

client = boto3.client('resourcegroupstaggingapi')


def get():
    response = client.get_resources(
        TagFilters=[
            {
                'Key': 'owner',
                'Values': [
                    'fborchers',
                ]
            },
        ]
    )
    return response
