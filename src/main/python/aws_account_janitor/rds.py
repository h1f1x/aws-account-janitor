import boto3
from botocore.exceptions import ClientError

from .logging import log

client = boto3.client('rds')


def db_exists_for_snapshot(snapshot):
    try:
        client.describe_db_instances(
            DBInstanceIdentifier=snapshot['DBInstanceIdentifier'])
    except ClientError:
        # to lazy of parsing the correct Exception, sorry
        return False
    return True


def _delete_snapshots(snapshots):
    for snapshot in snapshots:
        sid = snapshot['DBSnapshotIdentifier']
        if not db_exists_for_snapshot(snapshot):
            log('deleting snapshot w/o db: {} ...'.format(sid))
            client.delete_db_snapshot(DBSnapshotIdentifier=sid)
        else:
            log('skipping snapshot: {}'.format(sid))


def cleanup_snapshots(snapshot_type='manual'):
    attrs = {'SnapshotType': snapshot_type}
    while True:
        result = client.describe_db_snapshots(**attrs)
        snapshots = result['DBSnapshots']
        _delete_snapshots(snapshots)
        if 'Marker' not in result:
            break
        attrs['Marker'] = result['Marker']
