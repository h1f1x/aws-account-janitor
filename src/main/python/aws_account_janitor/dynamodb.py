import boto3
from .logging import log

client = boto3.client('dynamodb')


def cleanup_backups(dry_run=False):
    for backups in client.get_paginator('list_backups').paginate():
        for backup in backups['BackupSummaries']:
            log_prefix = '[DRY RUN] ' if dry_run else ''
            log('{}deleting backup/table: {}/{} ...'.format(
                log_prefix, backup['BackupName'], backup['TableName']))
            if not dry_run:
                client.delete_backup(BackupArn=backup['BackupArn'])


def cleanup_tables(dry_run=False):
    for tables in client.get_paginator('list_tables').paginate():
        for table in tables['TableNames']:
            log_prefix = '[DRY RUN] ' if dry_run else ''
            log('{}deleting table: {} ...'.format(
                log_prefix, table))
            if not dry_run:
                client.delete_table(TableName=table)
