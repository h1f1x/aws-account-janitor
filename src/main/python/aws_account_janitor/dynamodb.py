import boto3
from .logging import log

client = boto3.client('dynamodb')


def cleanup_backups(dry_run):
    for backups in client.get_paginator('list_backups').paginate():
        for backup in backups['BackupSummaries']:
            log_prefix = '[DRY RUN] ' if dry_run else ''
            log('{}deleting backup/table: {}/{} ...'.format(
                log_prefix, backup['BackupName'], backup['TableName']))
            if not dry_run:
                client.delete_backup(BackupArn=backup['BackupArn'])
