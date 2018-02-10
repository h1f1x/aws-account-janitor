import boto3
import click
import time

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


def wait_for_status_change(status, timeout):
    cf = boto3.client('cloudformation')
    all_stacks_changed = False
    click.echo('Looking for {} stacks and wait (max. {}s) for them to change their status.'.format(
        status, timeout))
    wait_until = time.time() + timeout
    pending = {n['StackName'] for n in cf.list_stacks(
        StackStatusFilter=status.split())['StackSummaries']}
    log('>> Found {} stacks.'.format(len(pending)))
    for stack in pending:
        log('- {}'.format(stack))
    log('Waiting ...')

    while True:
        if len(pending) < 1:
            print('<< Voila, all found stacks changed its status.')
            all_stacks_changed = True
            break
        if time.time() >= wait_until:
            print('<< Got bored of waiting. Timeout after: {} s.'.format(timeout))
            break
        time.sleep(2)
        stacks = {n['StackName'] for n in cf.list_stacks(
            StackStatusFilter=status.split())['StackSummaries']}
        changed = pending - stacks
        for stack in changed:
            log('{} - changed status'.format(stack))
        pending = stacks & pending
    return all_stacks_changed
