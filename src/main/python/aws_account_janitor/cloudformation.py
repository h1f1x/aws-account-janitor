import boto3
import click

from aws_account_janitor.logging import log


def get_stacknames_by_status(status):
    cf = boto3.client('cloudformation')
    result = cf.list_stacks(StackStatusFilter=[status])
    stacks = result['StackSummaries']
    return [s['StackName'] for s in stacks]


def cleanup(status, interactive=True):
    cf = boto3.client('cloudformation')
    log('Looking out for {} stacks ...'.format(status))
    stacks = get_stacknames_by_status(status)
    for stack_name in stacks:
        print('found: {}'.format(stack_name))
    if len(stacks) < 1:
        log('no stack found with status: {}'.format(status))
        return
    if not interactive or click.confirm('Should we delete the above stacks?'):
        click.echo('Ok, gonna take some time to delete multiple stacks ...')
        for stack_name in stacks:
            log('initiating deletion of "{}" ...'.format(stack_name))
            cf.delete_stack(StackName=stack_name)
